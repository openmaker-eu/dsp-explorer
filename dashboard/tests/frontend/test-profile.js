describe('test profile', function() {
    
    beforeEach(function(){
        browser.manage().window().setSize(1600, 1000);
        browser.get('http://localhost:8000');
        browser.waitForAngular();
        browser.ignoreSynchronization = true;
    });
    
    it('should open a page', function() {
        console.log('[assert open an html page]');
        expect($('body').isPresent()).toBe(true);
    })
    
    it('should open login modal', function() {
        console.log('[assert opens the login modal]');
        
        let login_modal = $('#login_modal')
        let open_modal_button = $('[ng-click="openModal(\'#login_modal\')"]')
        open_modal_button.click()
        
        browser.wait(open_modal_button, 10000);
        expect(open_modal_button.isDisplayed()).toBe(true);
    })
    
    // it('should login', function() {
    //     console.log('[assert login]');
    //
    //     $('#login_modal input[name="email"]').clear().sendKeys('santoli.massimo@top-ix.org');
    //     $('#login_modal input[name="password"]').clear().sendKeys('q1w2e3r4');
    //     $('#login_modal button[type="submit"]').click()
    //     expect(true).toBe(true);
    //
    // });

    
});