import logging

from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import get_settings

settings = get_settings()


def setup_otel(app: FastAPI):
    # Resource: shared service-level metadata (e.g. service.name)
    resource = Resource(attributes={SERVICE_NAME: settings.service_name})

    # Logs: LoggerProvider with OTLP HTTP exporter
    log_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint=settings.log_otlp_endpoint)
    log_processor = BatchLogRecordProcessor(
        log_exporter,
        max_export_batch_size=512,
        max_queue_size=2048,
        schedule_delay_millis=2000,
        export_timeout_millis=30000,
    )
    log_provider.add_log_record_processor(log_processor)
    # Register global LoggerProvider
    set_logger_provider(log_provider)
    # Bridge Python logging to OpenTelemetry Logs
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=log_provider)
    logging.getLogger().addHandler(handler)

    # Metrics: MeterProvider with periodic OTLP export
    metric_exporter = OTLPMetricExporter(endpoint=settings.metric_otlp_endpoint)
    metric_reader = PeriodicExportingMetricReader(
        metric_exporter, export_interval_millis=60000, export_timeout_millis=30000
    )
    metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(metric_provider)

    # Traces: TracerProvider with batch span processing
    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=settings.tracer_otlp_endpoint)
    trace_processor = BatchSpanProcessor(
        trace_exporter,
        max_export_batch_size=512,
        max_queue_size=2048,
        schedule_delay_millis=2000,
        export_timeout_millis=30000,
    )
    trace_provider.add_span_processor(trace_processor)

    # Register global TracerProvider
    trace.set_tracer_provider(trace_provider)

    # Automatically create spans for FastAPI requests
    FastAPIInstrumentor().instrument_app(app)

    # Inject trace_id and span_id into application logs
    LoggingInstrumentor().instrument(set_logging_format=True)
