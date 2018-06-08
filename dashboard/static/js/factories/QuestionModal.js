
let template = `
    <div class="modal-body padding-5-perc">
        <wizard questions="preset" action="action"></wizard>
    </div>
`

export default ['$rootScope', '$uibModal', function($rootScope, $uibModal){
    let F = {
        open: (ev,preset,action=null)=>{
            F.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                transclude:true,
                controller: ['$scope', '$http', function($scope, $http){
                    $scope.preset=preset
                    $scope.action=action
                    // Get questions from backend if not provided to directive
                    !$scope.preset && $http
                        .get('/api/v1.4/questions/' + ( $scope.action ? '?action='+$scope.action : '') )
                        .then(res=>$scope.preset=res.data.questions)
                }]
            });
        },
        close:()=>F.modalInstance.close()
    }
    
    $rootScope.$on('question.modal.open', F.open)
    $rootScope.$on('question.modal.close', F.close)
    
    return F

}]