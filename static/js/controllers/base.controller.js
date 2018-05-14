import * as _ from 'lodash'
export default
            ['$scope','$http','$rootScope','toastr','MessageModal','QuestionModal','LoginService',
    function ($scope, $http, $rootScope, toastr, MessageModal, QuestionModal, LoginService) {
    
    // GLOBAL ACTIONS
    $scope.open_signup = ($event)=> { $event.stopPropagation(); $rootScope.$emit('question.modal.open') }
    $scope.logout =()=>LoginService.logout()
    $scope.login =()=>$rootScope.$emit('question.modal.open', [
        {name:'login', type:'login', label:'Insert your credentials', apicall: '/api/v1.4/login/', emitevent:'authorization.refresh'},
        {name:'end', type:'success', label: 'Successful login', }
    ])
    
    // TOASTR
    $scope.$watch('toastrMessage', function (newValue, oldValue) {
        _.forEach( newValue, (el) => {
            
            el.tags = el.tags.split(" ")
            let toastr_tags = [ 'debug', 'info', 'success', 'warning', 'error' ]
            
            // Is a Modal
            if( el.tags.indexOf('modal') > -1 ){
                try{
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

}]

