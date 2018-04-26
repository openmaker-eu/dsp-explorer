let template = `
    <div class="container ">
        <div class="row">
            
            <!--Entity Heading-->
            <div class="col-md-12 entity-heading margin-bottom-1-perc">
                <div class="row">
                   <h1 class="col-md-9 col-sm-9 col-sm-offset-0">
                       <span class="entity-detail__title">{$ entityname $}</span>
                       <span class="pull-right">
                           <bookmark-button entityname="{$ entityname $}" entityid="{$ entityid $}"></bookmark-button>
                           <interest-button entityname="{$ entityname $}" entityid="{$ entityid $}"></interest-button>
                       </span>
                   <h1>
                </div>
            </div>
            
            <div class="col-md-9 col-sm-9 col-sm-offset-01 entity-detail-page__content">
                
                <!--Content-->
                <div class="row entity-detail__content">
                    <div class="col-md-8">
                        
                        <!--Loader-->
                        <entity-loading
                            loading="!entity.data && !nodata"
                            nodata="nodata"
                            entityname="{$ entityname $}"
                        ></entity-loading>
                        
                        <!-- Enitiy details -->
                        <div ng-if="entity.data !== null">
                            <entity-detail entity="entity.data" entityid="{$ entityid $}" entityname="{$ entityname $}" ></entity-preview>
                        </div>
                        <br>
                        
                    </div>
                    <div class="col-md-4">
                        
                        <!--Challenges: Event details with icons-->
                        <div
                            ng-if="{$ entityname == 'challenge' $}"
                            style="display: flex; flex-direction: row; justify-content:left; align-items:center; "
                         >
                                <hh5><i class="fa fa-calendar"></i>&nbsp;&nbsp;&nbsp;&nbsp;</hh5>
                                <h5>{$ entity.data.start_date | date:'d MMMM yyyy' $}</h5>
                                <h5>&nbsp;-&nbsp;</h5>
                                <h5>{$ ( entity.data.end_date | date:'d MMMM yyyy') || 'In progress' $}</h5>
                        </div>
                        
                        <img style="padding:0; width:100%;" ng-src="{$ entity.data.im || entity.data.picture || entity.data.cover $}" class="col-md-12">
                        
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
        controller : ['$scope', '$http','EntityProvider', async function($scope, $http, EntityProvider) {
            
            $scope.slider_list = $scope.slider ? $scope.slider.split('-').filter(x => x): []
            $scope.entity = EntityProvider.make($scope.entityname,$scope.entityid)
            $scope.nodata = !$scope.entity.get()

        }]
    }
}]



