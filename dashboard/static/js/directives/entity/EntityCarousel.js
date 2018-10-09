let _ = require("lodash");

let template = `
    <div>
        <div class="entity-carousel entity-carousel--{$ entityname $} entity--{$ entityname $}" >
        
            <div class="entity-carousel__header ">
                <h4 ng-if="!carouseltitle"><a href="/entity/{$ entityname $}" ng-bind-html="entitiy_title()"></a></h4>
                <h4 ng-if="carouseltitle" ng-bind-html="carouseltitle"></h4>
            </div>
            
            <entity-loading
                class="text-{$ entityname $} text-center"
                loading="entity_list.loading"
                entityname="{$ entityname $}"
                error="entity_list && !entity_list.loading && entity_list.data && entity_list.data.length===0"
                errormessage="error_message"
             ></entity-loading>
            
            <div
                class="entity-carousel__body"
                ng-class="{'small-slider': entityperslide > 1}"
                ng-if="entity_list && !entity_list.loading && entity_list.data.length!==0">
                <slick settings="slickConfig" >
                    <div ng-repeat="entity in entity_list.data | limitTo: (limit || 20)" >
                        <entity-detail entity="entity" entityname="{$ entityname $}" preview="true"></entity-detail>
                    </div>
                </slick>
            <div>
            
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        transclude:false,
        scope: {
            entityid : '@',
            entityname : '@',
            userid: '@',
            user: '=',
            slider : '@',
            limit: '=',
            entityperslide: '@',
            carouseltitle : '@'
        },
        controller : ['$scope', '$rootScope', '$http', '$timeout', 'EntityProvider', function($scope, $rootScope, $http, $timeout, EntityProvider) {
            $scope.is_my_profile = false
            $scope.error_message = false
            $scope.username = ''
            $scope.entity_list = EntityProvider.make($scope.entityname, $scope.entityid, $scope.userid)
            $scope.entity_list.get()
            
            $scope.set_user_dependent_vars = () =>{
                $scope.is_my_profile = $scope.userid && $scope.userid == $rootScope.user.profile
                $scope.username = _.get($scope.user, 'data.user.first_name')
                $scope.error_message = $scope.get_error_message()
            }
    
            $scope.$watch('user.data', $scope.set_user_dependent_vars)
            $rootScope.$watch('user', $scope.set_user_dependent_vars)
            
            $scope.entitiy_title= ()=> ['challenges', 'projects'].includes($scope.entityname)
                ? '<span>Projects&nbsp;/&nbsp;</span><span class="text-yellow">Challenges</span>'
                : $scope.entityname == 'news' ? 'articles' : $scope.entityname
            
            $scope.get_error_message= () =>
                $scope.entityname === 'lovers' && $scope.is_my_profile && 'There are no people who have shown interest in you ' ||
                $scope.entityname === 'lovers' && 'There are no people who have shown interest in '+$scope.username +'. You can show your interest in '+$scope.username+' by clicking on the heart shaped icon' ||
                
                $scope.entityname === 'loved' && $scope.is_my_profile && 'You have not shown interest in anyone' ||
                $scope.entityname === 'loved' && $scope.username+' don\'t shows interest to anyone' ||
                
                $scope.entityname === 'matches' && $scope.is_my_profile && 'Currently there are no people similar to you' ||
                $scope.entityname === 'matches' && 'Currently there are no people similar to '+$scope.username ||
                
                false
            
            $scope.$watch('entity_list.data',  (a, b)=>{
                $scope.reload = true;
                $timeout(function(a){ $scope.reload=false, $scope.nodata= !a || a.length===0 },1000);
            })
    
            $scope.slickConfig ={
                slidesToShow: $scope.entityperslide || 1,
                slidesToScroll: $scope.entityperslide || 1,
                prevArrow: '<i class="fas fa-chevron-left slick-arrow--custom prev"></i>',
                nextArrow: '<i class="fas fa-chevron-right slick-arrow--custom next"></i>',
    
                //focusOnSelect: false,
                autoplay: false,
                draggable: true,
                infinite: true,
                pauseOnHover: true,
                swipeToSlide: true,
                arrows: true,
                //accessibility: true,
                adaptiveHeight: false
            }
            
        }]
    }
}]

var row_html = '' +
    '<section class="row section-activities--mobile">' +
    '<div class="spb-row " data-row-type="color" data-wrap="full-width-contained" data-image-movement="fixed" data-content-stretch="false" data-row-height="content-height" data-col-v-pos="default" data-legacy="true" style="margin-top: 0px; margin-bottom: 0px; opacity: 1; visibility: visible;" data-sb-init="true">' +
    '<div class="spb_content_element clearfix" style="padding-left: 383px; padding-right: 382px;">' +
    '<div class="spb-row-no-cols-wrapper spb-row-multi-col clearfix"> ' +
    '<div class="row">' +
    '<div class="blank_spacer col-sm-12></div>'
'</div>'+
'</div>' +
'</div>'+
'</div>' +
'</section>'

var row_html = '' +
    '<section class="row section-activities--mobile">' +
    '<div class="spb_content_element col-sm-12 spb_text_column">' +
    '<div class="spb-asset-content" style="padding-top:0%;padding-bottom:0%;padding-left:0%;padding-right:0%;">' +
    '<div class="title-wrap clearfix ">' +
    '<h2 class="spb-heading"><span>Attività</span>' +
    '</h2>' +
    '</div>' +
    '</div>'+
    '</div>'+
    '</section>'
