export default ['$scope','$uibModal','$http','$rootScope','toastr', function ($scope,$uibModal,$http,$rootScope,toastr) {
    
    $scope.rootScope = $rootScope;
    
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
        newValue.forEach(function (el) {
            toastr[el.tags](el.message);
        })
    })

}]