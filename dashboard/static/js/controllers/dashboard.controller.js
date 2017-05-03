/**
 * Created by andreafspeziale on 03/05/17.
 */
export default [ '$scope','$uibModal', function ($scope,$uibModal) {

    console.log('dashboard controller')

    let modals = {
        'login':'',
        'invite':'',
        'membership':require('../templates/modals/request_membership.html')
    }

    $scope.openModal = (m) => {
        $scope.modalInstance = $uibModal.open({
            template: modals[m],
            controller: 'dashboardController',
            backdrop: 'static',
            scope:$scope
        });
    }

    $scope.closeModal = () => {
        $scope.modalInstance.close();
    }
}]