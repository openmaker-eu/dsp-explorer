
let template = `
    <div ng-repeat="entity_name in entities_names" class="col-md-4">
        <entity-carousel entityname="{$ entity_name $}" limit="$root.authorization<10 && 1"></entity-carousel>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {},
        controller : ['$scope', function($scope) {
            $scope.entities_names = ['news', 'events', 'projects']
        }]
    }
}]



