import * as _ from 'lodash'
export default
    ['$scope','$uibModal','$http','$rootScope','toastr','MessageModal', 'ModalFactory', 'SignupModal', '$timeout', 'LoginService',
    function ($scope,$uibModal,$http,$rootScope,toastr, MessageModal, ModalFactoryl, SignupModal, $timeout, LoginService) {
    
    $scope.openModal = (m) => {
        let modal = $(m);
        if( modal.length>0 ){
            $scope.modalInstance = $uibModal.open({
                template: modal.html(),
                backdrop: 'static',
                scope: $scope
            });
        }
    }
    
    $scope.closeModal = () => { $scope.modalInstance.close();  $scope.modal_message = null;}
    
    $scope.modal_message = null;
    
    $scope.$watch('toastrMessage', function (newValue, oldValue) {
        _.forEach( newValue, (el) => {
            
            el.tags = el.tags.split(" ")
            let toastr_tags = [ 'debug', 'info', 'success', 'warning', 'error' ]
            
            // Is a Modal
            if( el.tags.indexOf('modal') > -1 ){
                try{

                    console.log(el.message);

                    let modal_options = JSON.parse( el.message );
                    modal_options.body = modal_options.body.replace(/ESCAPE/g, '"');
                    modal_options.title
                        && modal_options.body
                        && MessageModal.openModal(
                            modal_options.title || null,
                            modal_options.body || null,
                            null,
                            null,
                            null,
                            modal_options.footer
                        )
                }
                catch(e){console.log('[ERROR] : modal message object is not valid');}
                return
            }
            // Is a Toastr
            else
            {
                _.forEach(el.tags, (tag)=>{
                    let tag_index = toastr_tags.indexOf(tag)
                    if(tag_index > -1) toastr[toastr_tags[tag_index]](el.message);
                })
            }
            
        })
    })
    
    
    $scope.open_signup = ()=>{ $rootScope.$emit('signup.modal.open') }

    // LOGIN
    $scope.logout =()=>LoginService.logout()
    $scope.login =()=>LoginService.login()

    }]

