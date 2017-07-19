import * as _ from 'lodash'

export default [ '$uibModal', '$rootScope', function($uibModal, $rootScope) {
    
    let scope = $rootScope;
    let setDependencyToScope = (controller) => {
    
        let args = controller.toString().match(/\((?:.+(?=\s*\))|)/)[0].slice(1).split(/\s*,\s*/g);
        let stringArgs = _.map(args, arg => '"'+arg+'"')
        
        let new_controller = function () {}
        eval(`new_controller = [${ _.join(stringArgs, ",") }, function (${ _.join(args, ",") }){
        
                if( $scope && $scope!==undefined) {
                    ${ _.reduce(args, (carry, arg)=>{
                
                        if( arg !== '$scope') carry += '$scope["'+arg+'"] = '+arg+' ;'
                        return carry
                        
                    }, '') }
                };
                
                controller(${ _.join(args, ",") });
                
            }];`);
        
        return new_controller;
        
    }
    
    var modalObject = {
        
        modalFactory : $uibModal,
        modalInstance : {},
        selected: {},
        
        createModal : (templateUrl, Controller = null) => {
            
            // Merge this and scope
            _.forOwn( modalObject, ( ConfProp, ConfKey ) => { scope[ConfKey] = ConfProp; })
            
            // Set all the dependecy as scope vars
            Controller = Controller ? setDependencyToScope(Controller): Controller;
            
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




