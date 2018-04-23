
let template = `
    <div class="container">
        <div class="row margin-top-5-perc margin-bottom-5-perc">
            <div class="home-page">
                <div ng-repeat="entity_name in entities_names " class="col-md-4">
                    <entity-carousel entityname="{$ entity_name $}" limit="$root.authorization<10 && 1"></entity-carousel>
                </div>
                <div ng-if="$root.authorization<10" class="text-center col-md-12 ">
                    <a href="/onboarding" class="btn btn--white btn-lg btn--big ">LOAD MORE</a>
                </div>
            </div>
        </div>
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



