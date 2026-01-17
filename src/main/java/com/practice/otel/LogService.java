package com.practice.otel;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class LogService {

    public void testLog() {
        log.info("LogService가 호출되었습니다.");
    }
}
