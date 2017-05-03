/**
 * Created by andreafspeziale on 03/05/17.
 */
export default [ '$scope','$uibModal','$http', function ($scope,$uibModal,$http) {
    
    this.openModal = (m) => {
        
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

    $scope.closeModal = () => {
        $scope.modalInstance.close();
    }
    
    $scope.request_membership = (email) => {
        $http({
            'method':'GET',
            'url' : '/request_membership/'+email
        }).then(
            r => {
                console.log(r);
                },
            e => {
                console.log(e);
            }
        )
    }
    
}]