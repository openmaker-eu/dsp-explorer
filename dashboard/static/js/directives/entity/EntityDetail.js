
let template = `
    <div class="entity--{$ entityname $} entity-detail"
        ng-class="{
            'background-challenge--light': entity.hasOwnProperty('company'),
            'background-white': ! entity.hasOwnProperty('company') && preview
        }">
        
        <div
            ng-class="{'force-square': preview}"
            ng-if="['lovers','loved','matches'].includes(entityname) && entity.picture"
        >
                <a ng-href="{$ entity.id? '/profile/'+entity.id : '' $}" class="entity-detail__username"
                ><span>{$ entity.user.first_name+' '+entity.user.last_name $}</span></a>
                <circle-image
                    src="entity.picture"
                    href="/profile/{$ entity.id $}"
                    squared="true"
                    placeholder="{$ '/media/images/profile/'+entity.gender+'.svg' $}"
                ></circle-image>
        </div>
        
        <div ng-class="{'force-square': preview}" ng-if="entityname==='profile'">Profile Page</div>
        <div ng-class="{'force-square': preview}" ng-if="['projects','challenges','news','events'].includes(entityname)">
          
            <!--Fade container-->
            <a ng-href="{$ entity_link() $}" ng-if="preview" class="fade"></a>
            
            <div class="entity-detail__content entity-detail-padding" >
                
                <!--Entity Detail Title-->
                <h3 class=" entity-detail__title semi-bold" style="letter-spacing: 1px;">
                    <!--<span>{$ entity.title || entity.name | limitTo: ( preview ? 50 : '' ) $}</span>-->
                    <!--<span ng-if="preview && entity.title.length > 20">...</span>-->
                    
                    <a
                        ng-if="!preview && (entity.link || entity.source)"
                        ng-href="{$ entity.link || entity.url $}"
                        class="text-{$ entityname $}"
                        target="_blank"
                    >
                        {$ entity.title || entity.name | limitTo: ( preview ? 100 : '' ) $}
                    </a>
                    
                    <span
                        ng-if="preview || !(entity.link || entity.source)"
                        class="text-{$ entityname $}"
                    >
                        {$ entity.title || entity.name | limitTo: ( preview ? 100 : '' ) $}
                    </span>
                    
                </h3>
                <br>
                
                <!--PROJECTS ONLY: Company title with icons-->
                <div ng-if="entityname == 'projects'"">
                    <h5 ng-if="entity.profile.user">
                        <a ng-href="/profile/{$ entity.profile.id $}">
                            <i class="fas fa-fw fa-user-tie" style="font-size:120%;"></i>&nbsp;&nbsp;
                            <span class="cairo">{$ entity.profile.user.first_name $} {$ entity.profile.user.last_name $} ({$ entity.creator_role $})</span>
                        </a>
                    </h5>
                    <h5 ng-if="entity.tags">
                        <i class="fas fa-fw fa-hashtag" style="font-size:120%;"></i>&nbsp;&nbsp;
                        <span ng-repeat="tag in entity.tags" class="cairo">
                             <span style="line-height: 150%;" class="text-grey--dark">#</span>{$tag.name$}</span>&nbsp;&nbsp;
                        </span>
                    </h5>
                    <h5 ng-if="entity.project_url" ><a ng-href="{$ add_http_to_url(entity.project_url) $}" target="_blank">
                            <i class="fas fa-fw fa-link" style="font-size:120%;"></i>&nbsp;&nbsp;
                            <span">{$ entity.project_url $}</span>
                        </a>
                    </h5>
                    </br>
                </div>
                
                <!--CHALLENGES ONLY: tags-->
                <span ng-if="entityname == 'challenges'" class="entity-detail__event-detail">
                    <span style="margin:0; padding:0;">
                        <img style="max-height: 30px;" ng-src="{$ entity.company.logo $}" alt="">&nbsp;
                        <span>{$ entity.company.name $}</span>
                    </span>
                    </br>
                </span>

                <!--EVENT ONLY: Event details with icons-->
                <div ng-if="entityname == 'events'" class="entity-detail__event-detail entity-detail__body">
                    <p><i class="far fa-calendar-alt"></i>&nbsp;&nbsp;
                    {$ entity.start_time | date:'d'  $}
                    {$ entity.start_time | date:'MMMM' | uppercase  $}
                    {$ entity.start_time | date:'yyyy, EEEE' $}
                    </p>
                    <p ng-if="entity.place"><i class="fas fa-map-marker-alt bold"></i>&nbsp;&nbsp;{$ entity.place | uppercase $}</p>
                    <p><a href="{$ entity.link $}" target="_blank"><i class="far fa-calendar-plus"></i><span>&nbsp;&nbsp;REGISTER</span></a></p>
                    <br>
                </div>
  
                <!--Read more-->
                <a ng-if="entityid && preview" ng-href="{$ entity_link() $}" class="read-more entity-detail-padding"><h4>READ MORE</h4></a>

                <!-- Show Full text if exist-->
                
                    <!--News-->
                    <p class="entity-detail__body" ng-if="entity.full_text">
                        <span>{$ entity.summary | limitTo : 1024 $}</span>
                        <span ng-if="entity.description.text.length > 1024">&nbsp;<a target="_blank" ng-href="{$ entity.link || entity.url $}">
                        <i class="fas fa-angle-double-right"></i></a></span>
                    </p>

                    <!--Events-->
                    <p class="entity-detail__body" ng-if="entity.description.text">
                        {$ entity.description.text | limitTo : 1024 $}
                        <span ng-if="entity.description.text.length > 1024">&nbsp;<a target="_blank" ng-href="{$ entity.link || entity.url $}">
                            <i class="fas fa-angle-double-right"></i>
                        </a></span>
                    </p>
                    
                    <!--Projects-->
                    <p class="entity-detail__body" ng-if="entity.description && !entity.description.text" >
                        <span ng-if="preview">
                            {$ entity.description | limitTo : 512 $}
                            <span ng-if="entity.description.length > 512">...</span>
                        </span>
                        <span ng-if="!preview">
                            {$ entity.description $}
                        </span>
                    </p>
                    
                    <!--Challenges-->
                    <span class="entity-detail__body" ng-if="entity.details" ng-bind-html="entity.details"></span>
                    
                    <!--link to source-->
                    <h5 ng-if="!preview && (entity.link || entity.source)" class="text-red">
                    <br>
                        <a href="{$ entity.link || entity.url $}" target="_blank">Go to source</a>
                    </h5>
   
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
            
            $scope.add_http_to_url = (url)=>url.startsWith("http://") || url.startsWith("https://") ? url : 'http://'+url
    
            const new_image = (src)=>{
                let image = new Image()
                image.src = src
                image.className = "circle-image portrait"
                return image
            }
            
        }]
    }
}]



