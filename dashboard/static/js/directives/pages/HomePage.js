
let template = /*html*/`
    <div class="container home-page">
        <div class="row row--mobile">
            <h3 class="col-md-12 margin-top-2-perc"><a class="text-red cairo bold" href="/manifesto">OM MANIFESTO</a></h3>
        </div>
        <div class="row margin-top-2-perc margin-bottom-5-perc">
            <div ng-repeat="entity_name in entities_names" class="col-md-4">
                <entity-carousel entityname="{$ entity_name $}" limit="$root.authorization<10 && 1"></entity-carousel>
            </div>
            <div ng-if="$root.authorization<10" class="text-center col-md-12 margin-top-5-perc">
                 <span ng-click="open_login()" class="btn btn--white btn-lg btn--big pointer">LOAD MORE</span>
            </div>
        </div>
    </h3>
`

export default [function(){
    return {
        template:template,
        scope: {},
        controller : ['$scope', '$rootScope', function($scope, $rootScope) {
            $scope.entities_names = ['news', 'events', 'projects']
            $scope.open_login = ()=>{ $rootScope.$emit('question.modal.open') }
            $scope.test = ''
        }]
    }
}]
