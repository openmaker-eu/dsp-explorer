import * as _ from 'lodash'

let template = /*html*/`
    <div class="container entity-list">
        <div class="row ">
        
            <!--Entity heading-->
            <div class="mobile__padding">
            <div class="entity-list__title entity-heading col-md-12 col-sm-12">
                <div class="row">
                    <h2 class="col-md-9 col-sm-9 col-sm-offset-0 page-title">
                       <span class="entity-detail__title">
                            <span ng-if="entityname !== 'projects'" ng-bind-html="entitiy_title()"></span>
                            <span ng-if="entityname === 'projects'" >Projects / <span class="text-red">Challenges</span></span>
                       </span>
                       
                       <span ng-if="$root.authorization>=10 && entityname === 'projects'">
                            <a href="/profile/project/"><i class="fa fa-plus-circle text-{$ entityname $}"></i></a>
                       </span>
                       
                       <span class="pull-right">
                            <bookmarked-stripe-toggler
                            tooltip-placement = 'bottom-left'
                            uib-tooltip-html="'<big>Show/Hide bookmarked {$ entityname == 'news' ? 'articles' : entityname $}</big>'"
                            entityname="{$ entityname $}"></bookmarked-stripe-toggler>
                       </span>
                       <h1>&nbsp;</h1>
                   <h2>
                </div>
            </div>
        
            <!--Left content-->
            <div class="col-md-9 col-sm-9 col-sm-offset-0 entity-content" >
                <div class="row">
                    
                    <div class="col-md-12">
    
                        <entity-loading
                            loading="entities.data.length==0 && !nodata || force_loading"
                            error="nodata"
                            entityname="{$ entityname $}"
                        ></entity-loading>
                        
                    </div>
    
                    <div ng-if="entities.data.length > 0 && !force_loading" >
                    
                        <bookmarked-stripe entityname="{$ entityname $}"></bookmarked-stripe>
                    
                        <!--Entity list-->
                        <div
                            class="col-lg-4 col-md-6 col-sm-12 col-xs-12 "
                            ng-repeat="entity in entities.data"
                            style="margin-bottom:1%; margin-top: 1%;"
                        >
                            <div class="entity-list__box">
                                <entity-detail
                                    entity="entity"
                                    entityname="{$ entityname=='projects' && entity.hasOwnProperty('company')? 'challenges' : entityname $}"
                                    entityid="{$ entity.link_id || entity.id $}"
                                    preview="true"
                                ></entity-detail>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row" ng-if="$root.authorization >= 10">
                    <div class="col-md-12">
                        <br><br>
                        <simple-pagination
                                prevfunction="prev"
                                nextfunction="next"
                                nextcursor="nextcursor"
                                prevcursor="prevcursor"
                        ></simple-pagination>
                        <br><br>
                    </div>
                    
                </div>
            </div>
            </div>
        
            <!--Right sidebar-->
            <div class="col-md-3" >
                <entity-sidebar slider="{$ slider $}" entityname="{$ entityname $}"></entity-sidebar>
            </div>
            
        </div>

    </div>
`

export default [function(){
    return {
        template:template,
        scope: {
            profileid : '=',
            entityname : '@',
            slider : '@'
        },
        controller : ['$scope', '$http', '$rootScope', 'EntityProvider', '$timeout', function($scope, $http, $rootScope, EntityProvider, $timeout) {
            
            // PAGINATION
            $scope.page = 0
            $scope.nextcursor = _.get($scope.entities, 'is_last_page')
            $scope.prevcursor = -1
            $scope.force_loading = false
            
            $scope.prev=()=>{
                $scope.page = $scope.page-1
                $scope.get_data()
            }
            
            $scope.next=()=>{
                $scope.page = $scope.page+1
                $scope.get_data()
            }
            
            $scope.get_data = ()=>{
                $scope.force_loading = true
                var response = $scope.entities.get(true , $scope.page)
                response.then((res)=>{
                    $scope.nextcursor = _.get($scope.entities, 'is_last_page') ? 0: 1
                    $scope.prevcursor = $scope.page
                    $scope.force_loading = false
                })
                return response
            }
    
            
            $scope.entities = EntityProvider.make($scope.entityname)
            $scope.data = $scope.get_data()
            $scope.nodata = !$scope.data
            
            $scope.data.then(
                ()=> $timeout(function(a){
                    $rootScope.$emit(`bookmarked.${$scope.entityname}.visibility`, {visible:$rootScope.page_info.bookmark})
                },1000)
            )
    
            // $rootScope.$emit(`bookmarked.${$scope.entityname}.visibility`, {visible:true})
            $scope.entitiy_title= ()=> ['challenges', 'projects'].includes($scope.entityname)
                ? '<span>Projects</span><span></span>&nbsp;/&nbsp;</span><span class="text-yellow">Challenges</span>'
                : $scope.entityname == 'news' ? 'articles' : $scope.entityname
    
        }]
    }
}]





