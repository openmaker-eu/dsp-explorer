
let template = `
    <div class="modal-body padding-5-perc modal-contact-user">
        <h2 class="">Contact {$ user && user.user.first_name $}</h2>
        <br>
        <div class="form-group" ng-class="{ 'has-error': is_submitted && message.length < 10 }">
            <label for="contact-user-email">
                Write an email message to {$ user && (user.user.first_name+' '+user.user.last_name) $}
                <span ng-if="is_submitted && message.length < 10" style="color:#a94442;">&nbsp;(Minimum 10 digits)</span>
            </label>
            <textarea
                id="contact-user-email"
                class="form-control"
                ng-model="message"
                cols="30" rows="10"
            ></textarea>
        </div>
        <br><br>
        
        <div class="form-gorup" ng-show="is_recaptcha_visible">
            <h5 ng-if="is_recapthca_submitted && !is_recaptcha_valid" class="text-danger text-right">Captcha is not valid</h5>
            <div
                vc-recaptcha
                key="key"
                ng-model="is_recaptcha_valid"
                theme="light"
                class="modal-contact-user__recaptcha"
                ng-class="{ 'captcha-error': !is_recaptcha_valid && is_recapthca_submitted }"
            ></div>
        </div>

        <div>
    
            <button class="btn btn-danger pull-right" ng-click="submit()">Invia</button>
            
            <span class="pull-right">&nbsp;&nbsp;</span>
            <button class="btn btn-default pull-right" ng-click="close()">Chiudi</button>
        </div>
        
    </div>
`

export default ['$rootScope', '$uibModal', '$document', function($rootScope, $uibModal, $document){
    
    let F = {
        open: ( user)=>{
    
            if($rootScope.modal_opened === true) return false
            
            F.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                transclude: true,
                appendTo : $document.find('.modal__container').eq(0),
                controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
                    
                    $scope.message = ''
                    $scope.user = user
                    $scope.close = F.close
                    
                    $scope.key= '6LdzQ3UUAAAAAB9vxZbCeZrOm_NBQ-vrmhjO46mw'
                    $scope.is_recaptcha_visible = false
                    $scope.is_recaptcha_valid = false
                    
                    $scope.is_submitted = false

                    $scope.submit = ()=>{
                        $scope.is_submitted = true;
                        $scope.is_recaptcha_visible && ($scope.is_recapthca_submitted = true);
                        $scope.message.length >=10 && ($scope.is_recaptcha_visible = true)
                        
                        
                        $scope.is_recaptcha_valid
                        && $http
                            .post(`/api/v1.4/contact/user/${ $scope.user.user.id }/`, {message:$scope.message})
                            .then(r=> F.close() && $rootScope.alert_message('success', 'Message sent'))
                            .catch(e=> F.close() && $rootScope.alert_message('danger', e))
                        
                    }
                }]
            });
    
            F.modalInstance.closed.then(n=>{})
            F.modalInstance.rendered.then(x=>x)
            F.modalInstance.opened.then(x=>x)
        },
        close:()=>F.modalInstance.close()
    }
    return F

}]
