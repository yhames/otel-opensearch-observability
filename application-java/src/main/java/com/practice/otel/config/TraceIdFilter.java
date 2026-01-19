package com.practice.otel.config;

import io.micrometer.tracing.TraceContext;
import io.micrometer.tracing.Tracer;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Objects;

/**
 * W3C Trace Context 표준에 따라 HTTP 응답 헤더에 traceparent 값을 추가하는 필터
 */
@Component
class TraceIdFilter extends OncePerRequestFilter {

    private static final String TRACEPARENT_HEADER = "traceparent";
    private static final String VERSION = "00";

    private final Tracer tracer;

    TraceIdFilter(Tracer tracer) {
        this.tracer = tracer;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        TraceContext context = this.tracer.currentTraceContext().context();

        if (Objects.nonNull(context)) {
            String traceId = context.traceId();
            String spanId = context.spanId();

            if (validateTraceContext(traceId, spanId)) {
                String sampled = Boolean.TRUE.equals(context.sampled()) ? "01" : "00";
                String traceparent = String.format("%s-%s-%s-%s", VERSION, traceId, spanId, sampled);
                response.setHeader(TRACEPARENT_HEADER, traceparent);
            }

        }

        filterChain.doFilter(request, response);
    }

    private static boolean validateTraceContext(String traceId, String spanId) {
        return Objects.nonNull(traceId) && Objects.nonNull(spanId);
    }

}

