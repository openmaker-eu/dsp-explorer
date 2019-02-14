const template = `
    <div class="col-md-12">
        <h3 class="">Delete Your account</h3>
        <br>
        <div class="alert alert-danger " role="alert">
                <p><i class="text-brown--dark">
                If you choose to permanently leave openmaker,
                you account will be deleted, you will not be able to login to openmaker explorer anymore.
             </i>
            </p>
            <br>
            <button class=" btn btn-danger" ng-click="open()">Delete My account</button>
            <span class="clearfix"></span>
        </div>
    </div>
`
const modal_template = `
            <div class="modal-content" >
                    <div class="modal-header" >
                        <button type="button" class="close" aria-label="Close" ng-click="close()"><span aria-hidden="true">&times;</span></button>
                        <h3 class="modal-title" id="myModalLabel">Account deletion</h3>
                    </div>
                    <div class="modal-body" style="font-size:1em;">
                       <p >This operation cannot be reverted, You will permanenlty loose all your data saved to OpenMaker Explorer</p>
                       <p>Are you sure do you want to delete your account?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" ng-click="close()">No, Close</button>
                        <button type="button" class="btn btn-default" ng-click="delete()">Yes, Delete my Account</button>
                    </div>
            </div>
`

export default function(){
    return {
        template:template,
        scope: {
        },
        controller : ['$scope', '$rootScope', '$uibModal', '$document', function($scope, $rootScope, $uibModal, $document){
    
            $scope.open = ()=> {
                const modal = $uibModal.open({
                    template: modal_template,
                    backdrop: true,
                    windowClass: '',
                    transclude: true,
                    appendTo : $document.find('.modal__container').eq(0),
                    controller: ['$scope', '$rootScope', '$http', '$window', function($scope, $rootScope, $http, $window){
                        
                        $scope.close = modal.close
                        $scope.delete=()=>{
                            $http.post('/api/v1.4/user/delete/')
                                .then(()=>{
                                    $window.location.href = '/#account_deleted'
                                })
                                .catch(e=>{
                                    console.log('error delete user', e.data.error);
                                    $rootScope.alert_message('danger', e.data.error)
                                    modal.close()
                                })
                            
                        }
            
                    }]
                });
            }
        
        }]
    }
}
