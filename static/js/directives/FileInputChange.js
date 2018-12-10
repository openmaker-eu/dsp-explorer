import * as _ from 'lodash'

export default [function() {
    return {
        scope : {
            inputFileModel:'=',
            inputFileForm : '='
        },
        controller: [ '$scope', '$element', function($scope, $element){
            
            $element.bind('change',(event)=> {
                    
                    let reader = new FileReader();
                    
                    reader.onload = (readerEvent) => {
                        $scope.inputFileModel = readerEvent.target.result
                        $scope.inputFileForm && _.set($scope, 'inputFileForm.$dirty', true)
                        $scope.$apply($scope)
                    }
                    reader.readAsDataURL(event.target.files[0]);
                    
                }
            );
            
        }]
    };
}];
