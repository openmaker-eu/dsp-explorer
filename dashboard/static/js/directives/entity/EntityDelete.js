import * as _ from 'lodash'
const template = `
    <h4 ng-click="open()"><i class="fas fa-trash-alt text-red" ></i></h4>
`
const modal_template = `
            <div class="modal-content" >
                    <div class="modal-header" >
                        <button type="button" class="close" aria-label="Close" ng-click="close()"><span aria-hidden="true">&times;</span></button>
                        <h3 class="modal-title" id="myModalLabel">Delete {$ entitydisplayname || entityname $}</h3>
                    </div>
                    <div class="modal-body" style="font-size:1em;">
                       <p>This operation cannot be reverted</p>
                       <p>Are you sure do you want to delete this {$ entitydisplayname || entityname $}?</p>
                       
                       <h3 class="alert alert danger" ng-if="error">{$  $}</h3>
                       
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" ng-click="close()">No, Close</button>
                        <button type="button" class="btn btn-default" ng-click="delete_entity()">Yes, Delete {$ entitydisplayname || entityname $}</button>
                    </div>
            </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entity : '=',
            entityname : '@',
            entitydisplayname : '@',
            entityid : '@',
        },
        controller : ['$scope', '$http', '$rootScope', '$uibModal', '$document', function($scope, $http, $rootScope, $uibModal, $document) {
            
            let entity = { entityname:$scope.entityname, entityid:$scope.entityid, entitydisplayname:$scope.entitydisplayname}
    
            $scope.open = ()=> {
                const modal = $uibModal.open({
                    template: modal_template,
                    backdrop: true,
                    appendTo : $document.find('.modal__container').eq(0),
                    controller: ['$scope', '$rootScope', '$http', '$window', function($scope, $rootScope, $http){
                        $scope.entityname = entity.entityname
                        $scope.entityid = entity.entityid
                        $scope.entitydisplayname = entity.entitydisplayname
                        $scope.close = modal.close
                        $scope.error = false
                        
                        $scope.delete_entity = () =>{
                            $http
                                .delete(`/api/v1.4/${entity.entityname}/${entity.entityid}/`)
                                .then(r=>{
                                    console.log(r);
                                    $rootScope.alert_message('success', `${$scope.entitydisplayname} deleted`);
                                    $rootScope.$emit('user.projects.refresh', {})
                                    modal.close()}
                                )
                                .catch(e=>$scope.error=e)
                        }
                
                    }]
                });
            }
            
        }]
    }
}]



