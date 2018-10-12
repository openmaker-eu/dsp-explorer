
let template = `
    <div class="modal-body padding-5-perc">
        <h2 class="">Contact {$ user && user.user.first_name $}</h2>
        <br>
        <p> Write an email message to {$ user && (user.user.first_name+' '+user.user.last_name) $}</p>
        <div>
            <textarea class="form-control" ng-model="message" cols="30" rows="10"></textarea>
        </div>
        <br><br>
        <div>
            <button class="btn btn-danger pull-right" ng-click="send()">Invia</button>
            <span class="pull-right">&nbsp;&nbsp;</span>
            <button class="btn btn-default pull-right" ng-click="close()">Chiudi</button>
        </div>
    </div>
`

export default ['$rootScope', '$uibModal', '$document', function($rootScope, $uibModal, $document){
    
    let F = {
        open: ( user)=>{
            
            console.log('open', open);
    
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
                    
                    $scope.send = ()=>{
                        $http
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
