import * as _ from 'lodash'

export default [ '$uibModal', '$rootScope', function($uibModal, $rootScope) {
    
    let scope = $rootScope;
    
    var modalObject = {
        
        modalFactory : $uibModal,
        modalInstance : {},
        selected: {},
        
        createModal : (templateUrl, Controller = null) => {
            
            // Merge this and scope
            _.forOwn( modalObject, ( ConfProp, ConfKey ) => { scope[ConfKey] = ConfProp; })
            
            // Create Modal
            return modalObject.modalInstance = $uibModal.open({
                template: templateUrl,
                backdrop: 'static',
                controllerAs: '$ctrl',
                controller: Controller,
                scope: scope,
                resolve: { 'self' : () => modalObject }
            });
            
        },
        
        closeModal :  ()=> { modalObject.modalInstance.dismiss('cancel'); },
        
    };
    
    return modalObject;
    
}];




