
let template = `
    <div class="modal-body padding-5-perc">
        <wizard questions="questions" wizardid="$id" configuration="{swipe:false}"></wizard>
        <navi-questions items="questions" wizardid="$id" nodots="action=='login'"></navi-questions>
    </div>
`

export default ['$rootScope', '$uibModal', '$document', function($rootScope, $uibModal, $document){
    
    let F = {
        open: (ev, questions, action=null)=>{
            
            console.log('modal', ev, questions, action);
            
            F.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                transclude: true,
                appendTo : $document.find('.modal__container').eq(0),
                controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
                    
                    $scope.questions=questions
                    $scope.action=action
                    
                    // Get questions from backend if not provided
                    !$scope.questions && $http
                        .get('/api/v1.4/questions/' + ( $scope.action ? $scope.action+'/' : '') )
                        .then(res=>$scope.questions=res.data.questions)
                    
                    $rootScope.$on('wizard.'+$scope.$id+'.end', F.close)
                    $rootScope.$on('question.modal.close', F.close)
                    
                    // force chatbot to stay closed
                    $rootScope.$emit('chatbot.force_close', true);
                    
                    $rootScope.noscroll = true

                }]
            });
    
            F.modalInstance.closed.then(n=>{
                // Allow chatbot to open
                $rootScope.$emit('chatbot.force_close', false);
                $rootScope.$emit('entity.change.all') ;
                $rootScope.$emit('authorization.refresh')
                $rootScope.noscroll = false
            })
    
            F.modalInstance.rendered.then(x=>x)
            F.modalInstance.opened.then(x=>x)
        },
        close:()=>F.modalInstance.close()
    }
    
    $rootScope.$on('question.modal.open', F.open)
    return F

}]