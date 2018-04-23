let template = `
    <div class="container entity-list">
        <div class="row">
        
           <!--Entity Heading-->
           <div class="col-md-12 entity-heading margin-bottom-1-perc">
                <div class="row">
                       <h1 class="col-md-9 col-sm-9 col-sm-offset-0">
                           <span class=" entity-detail__title">{$ entityname $}</span>
                           <span class="pull-right">
                               <bookmark-button entityname="{$ entityname $}" entityid="{$ entityid $}"></bookmark-button>
                               <interest-button entityname="{$ entityname $}" entityid="{$ entityid $}"></interest-button>
                           </span>
                       <h1>
                </div>
           </div>
    
           <div class="col-md-9 col-sm-9 col-sm-offset-01 entity-content">
                <!--Content-->
                <div class="row">
                    <div class="col-md-8">
                    
                        <!--Loader-->
                        <entity-loading
                            loading="!entity && !nodata"
                            nodata="nodata"
                            entityname="{$ entityname $}"
                        ></entity-loading>
                    
                        <!-- Enitiy details -->
                        <div ng-if="entity !== null">
                            <entity-detail entity="entity" entityid="{$ entityid $}" entityname="{$ entityname $}" ></entity-preview>
                        </div>
                        <br>
                    </div>
                    <div class="col-md-4">
                    
                        <!--EVENT ONLY: Event details with icons-->
                        <div ng-if="entityname == 'challenge'">
                            <p><i class="fa fa-calendar"></i>&nbsp;&nbsp;
                                <span>{$ entity.start_time | date:'d MMMM yyyy,EEEE' $}</span>
                                <span>{$ entity.end_time | date:'d MMMM yyyy,EEEE' $}</span>
                            </p>
                        </div>
                    
                        <img src="{$ entity.im || entity.picture || entity.cover $}" class="col-md-12" alt="single {$ entityname $} image">
                        
                    </div>
                </div>
            </div>
    
            <!--Right sidebar-->
            <div class="col-md-3">
                <entity-sidebar slider="{$ slider $}" entityname="{$ entityname $}"></entity-sidebar>
            </div>
            
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entityname: '@',
            entityid : '@',
            slider: '@'
        },
        controller : ['$scope', '$http', 'toastr', function($scope, $http, toastr,) {
            let url = ''

            $scope.entity = null
            $scope.nodata = false
            
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            
            $scope.get_data = (url) => {
                $scope.nodata = false;
                $http.get(url).then(res => {
                    $scope.entity = res.data.result[0] || null
                    $scope.nodata = res.data.result && res.data.result.length === 0
                },
                err => $scope.nodata = true
                )
            }
            
            $scope.get_data('/api/v1.4/' + $scope.entityname + '/details/' + $scope.entityid + '/')
    
        }]
    }
}]



