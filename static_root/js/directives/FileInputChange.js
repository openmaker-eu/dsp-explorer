import * as _ from 'lodash'

export default [function() {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            
                element.bind('change',(event)=> {
                    
                    let reader = new FileReader();
                    reader.onload = (readerEvent) => {
                        _.set(scope, attrs.inputFileModel, readerEvent.target.result)
                        scope.$apply(scope)
                    }
                    reader.readAsDataURL(event.target.files[0]);
    
                }
            );
        }
    };
}];