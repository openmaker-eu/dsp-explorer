exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['./dashboard/tests/frontend/test-profile.js'],
    allScriptsTimeout: 20000,
    jasmineNodeOpts: {
        showColors: true,
        isVerbose: true,
        includeStackTrace: true,
        // defaultTimeoutInterval: 60000  // 60 seconds
    }
};