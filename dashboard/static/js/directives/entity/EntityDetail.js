
let template = `
    <div class="entity--{$ entityname $} entity-detail"
        ng-class="{
            'background-challenge--light': entity.hasOwnProperty('company'),
            'background-white': ! entity.hasOwnProperty('company') && preview
        }">
        
        <div ng-class="{'force-square': preview}" ng-if="['lovers','loved','matches'].includes(entityname) && entity.picture">
            <a href="/profile/{$ entity.id $}">
                <img ng-src="{$ entity.picture || 'media/images/profile/other.svg' $}" alt="" style="width:100%;">
            </a>
        </div>
        
        <div ng-class="{'force-square': preview}" ng-if="entityname==='profile'">Profile Page</div>
        <div ng-class="{'force-square': preview}" ng-if="['projects','challenges','news','events'].includes(entityname)">
          
            <!--Fade container-->
            <a ng-href="{$ entity_link() $}" ng-if="preview" class="fade"></a>
            
            <div class="entity-detail__content entity-detail-padding" >
                
                <!--Entity Detail Title-->
                <h3 class="text-{$ entityname $} entity-detail__title semi-bold" style="letter-spacing: 1px;">
                    <!--<span>{$ entity.title || entity.name | limitTo: ( preview ? 50 : '' ) $}</span>-->
                    <!--<span ng-if="preview && entity.title.length > 20">...</span>-->
                    <span>{$ entity.title || entity.name | limitTo: ( preview ? 100 : '' ) $}</span>
                </h3>
                <br>
                
                <!--PROJECTS ONLY: Company title with icons-->
                <div ng-if="entityname == 'challenges'" class="entity-detail__event-detail">
                    <h4 style="margin:0; padding:0;">
                        <img style="max-height: 30px;" ng-src="{$ entity.company.logo $}" alt="">&nbsp;
                        <span>{$ entity.company.name $}</span>
                    </h4>
                    </br>
                </div>

                <!--EVENT ONLY: Event details with icons-->
                <div ng-if="entityname == 'events'" class="entity-detail__event-detail entity-detail__body">
                    <p><i class="far fa-calendar-alt"></i>&nbsp;&nbsp;
                    {$ entity.start_time | date:'d'  $}
                    {$ entity.start_time | date:'MMMM' | uppercase  $}
                    {$ entity.start_time | date:'yyyy, EEEE' $}
                    </p>
                    <p><i class="fas fa-map-marker-alt bold"></i>&nbsp;&nbsp;{$ entity.place | uppercase $}</p>
                    <p><a href="{$ entity.link $}" target="_blank"><i class="far fa-calendar-plus"></i><span>&nbsp;&nbsp;REGISTER</span></a></p>
                </div>
  
                <!--Read more-->
                <a ng-if="entityid && preview" ng-href="{$ entity_link() $}" class="read-more entity-detail-padding"><h4>READ MORE</h4></a>

                <!-- Show Full text if exist-->
                
                    <!--News-->
                    <p class="entity-detail__body" ng-if="entity.full_text ">
                        <span>{$ entity.summary | limitTo : 1024 $}</span>
                        <span ng-if="entity.description.text.length > 1024">...</span>
                    </p>

                    <!--Events-->
                    <p class="entity-detail__body" ng-if="entity.description.text">
                        {$ entity.description.text | limitTo : 1024 $}
                        <span ng-if="entity.description.text.length > 1024">...</span>
                    </p>
                    
                    <!--Projects-->
                    <p class="entity-detail__body" ng-if="entity.description && !entity.description.text">
                        {$ entity.description | limitTo : 1024 $}
                        <span ng-if="entity.description.length > 1024">...</span>
                    </p>
                    
                    <!--Challenges-->
                    <span class="entity-detail__body" ng-if="entity.details" ng-bind-html="entity.details"></span>
                    
                    <!--link to source-->
                    <p ng-if="!preview && (entity.link || entity.source)" class="text-red">
                        <a href="{$ entity.link || entity.url $}" target="_blank">Got to source</a>
                    </p>
   
            </div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            entity: '=',
            entityname: '@',
            entityid : '@',
            preview : '='
        },
        controller : ['$scope', '$sce', function($scope, $sce) {
            
            $scope.entity.details = $sce.trustAsHtml($scope.entity.details);
            $scope.entity_link = ()=> '/entity/' +
                $scope.entityname + '/' +
                ($scope.entityid || $scope.entity.id || $scope.entity.link_id ) + '/' +
                ($scope.entity.temp_id || '' )
        }]
    }
}]



