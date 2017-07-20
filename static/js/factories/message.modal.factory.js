export default ['$uibModal','$http','ModalFactory', function($uibModal,$http,ModalFactory) {
    return {
        openModal: function(title, message, button_title=null, button_url=null , action=null ){
            
            let controller = ($scope) => {
                $scope.title = title
                $scope.message = message
                $scope.button_title = button_title
                $scope.button_url = button_url
                $scope.button_action = action
            }
            
            this.modalInstance = ModalFactory.createModal(require('../../../templates/modals/message.html'), controller );
        }
    }
}];