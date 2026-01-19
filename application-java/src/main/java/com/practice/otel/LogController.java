package com.practice.otel;

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
}
