package com.practice.otel.controller;

import com.practice.otel.service.LogService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/logs")
public class LogController {

    private final LogService logService;

    @GetMapping("/test")
    public String GetLogTest() {
        log.info("/GET /logs/test 호출됨");
        logService.testLog();
        return "Logs generated successfully.";
    }

    @GetMapping("/error")
    public String GetLogError() {
        log.info("/GET /logs/error 호출됨");
        logService.testErrorLog();  // 의도적인 예외 발생
        return "Logs generated successfully.";
    }

}
