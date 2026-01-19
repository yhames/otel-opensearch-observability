package com.practice.otel.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class LogService {

    public void testLog() {
        log.info("LogService.testLog()가 호출되었습니다.");
    }

    public void testErrorLog() {
        log.info("LogService.testErrorLog()가 호출되었습니다.");
        throw new RuntimeException("의도적인 예외 발생");
    }

}
