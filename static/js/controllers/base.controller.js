export default [ '$scope','$uibModal','$http', function ($scope,$uibModal,$http) {
    
    $scope.openModal = (m) => {
        let modal = $(m);
        if( modal.length>0 ){
            $scope.modalInstance = $uibModal.open({
                template: modal.html(),
                controller: 'baseController',
                backdrop: 'static',
                scope: $scope
            });
        }

    }
    
    $scope.closeModal = () => { $scope.modalInstance.close(); $scope.modal_response = 'ciao'; }
    
    $scope.modal_response = {};
    $scope.request_membership = (email) => {
        
        console.log('oki');
        
        return $http({
            'method':'GET',
            'url' : 'request_membership/'+email+'/'
        })
        .then(
            r => {
                $scope.modal_response = { message: r.data.message , status : 'success' }
                console.log('modal_response', $scope.modal_response);
            }
            ,
            r => {
                if( r.data.hasOwnProperty('message') ) $scope.modal_response = r.data;
                else $scope.modal_response = { message: r.statusText , status : 'error' }
            }
        )
    }
    
    $scope.test = e => console.log($scope.modal_response);
    
}]