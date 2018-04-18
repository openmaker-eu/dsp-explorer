import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="entity--{$ entityname $}">
    
       <!--Header With title and actions-->
       <div class="col-md-8 col-md-offset-1 margin-bottom-1-perc">
           <h1 style="text-transform: uppercase">
               <span>{$ entityname $}</span>
               <span class="pull-right">
                   <bookmark-button entityname="{$ entityname $}" entityid="{$ entityid $}"></bookmark-button>
                   <interest-button entityname="{$ entityname $}" entityid="{$ entityid $}"></interest-button>
               </span>
           <h1>
       </div>


        <div class="col-md-8 col-md-offset-1 entity-content">
            <!--Content-->
            <div class="col-md-12">
            
                <!--Loader-->
                <entity-loading
                    loading="!entity && !nodata"
                    nodata="nodata"
                    entityname="{$ entityname $}"
                ></entity-loading>
            
                <!-- Enitiy details -->
                <div  ng-if="entity !== null">
                    <div>
                        <h2 class="text--{$ entityname $}">{$ entity.title || entity.name $}</h2>
                        <br>
                        <p ng-if="entity.lenght == 0">Loading data</p>
                        <p style="font-size:150%;">{$ entity.full_text || entity.description $}</p>
                    </div>
                    <br>
                    <entity-interested entityname="{$ entityname $}" entityid="{$ entityid $}"></entity-interested>
                </div>
                
            </div>
        </div>

        <!--Right sidebar-->
        <div class="col-md-3">
            <entity-sidebar slider="{$ slider $}" entityname="{$ entityname $}"></entity-sidebar>
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
        controller : ['$scope', '$http', 'toastr', '$rootScope', '$timeout', function($scope, $http, toastr, $rootScope, $timeout) {
            let url = ''

            $scope.entity = null
            $scope.nodata = false
            
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            
            $scope.get_data = (url) => {
                $http.get(url).then(res => {
                    $scope.entity = res.data.result[0] || null
                    $scope.nodata = $scope.entity.length === 0
                })
            }
            
            $scope.get_data('/api/v1.4/' + $scope.entityname + '/details/' + $scope.entityid + '/')
    
        }]
    }
}]



