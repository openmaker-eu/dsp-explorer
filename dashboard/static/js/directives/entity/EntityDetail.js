import * as _ from 'lodash'
import * as d3 from 'd3';
let template = `
    <div class="entity--{$ entityname $} entity-preview">
        <div ng-class="{'force-square': preview}">
            <div class="do-not-remove-me-please">
                
                <!--Entity Detail Title-->
                <h3 class="text-{$ entityname $}">
                    <span>{$ entity.title || entity.name | limitTo: 20 $}</span>
                    <span ng-if="entity.title.length > 20">...</span>
                </h3>
                <br>

                <!--EVENT ONLY: Event details with icons-->
                <div ng-if="entityname == 'events'" class="entity-preview__events-detail">
                    <p><i class="fa fa-calendar"></i>&nbsp;&nbsp;{$ entity.start_time | date:'d MMMM yyyy,EEEE' $}</p>
                    <p><i class="fa fa-map-marker"></i>&nbsp;&nbsp;{$ entity.place $}</p>
                    <p><a href="{$ entity.link $}" target="_blank"><i class="fa fa-plus-square"></i><span>&nbsp;&nbsp;REGISTER</span></a></p>
                </div>
                
                <!--Fade container-->
                <div ng-if="preview" class="fade"></div>
                
                <!--Read more-->
                <a ng-if="entityid && preview" href="/{$ entityname $}/{$ entityid $}" class="read-more"><h4>READ MORE</h4></a>

                <!-- Show Full text if exist-->
                <div>
                
                    <!--News-->
                    <p ng-if="entity.full_text">
                        {$ entity.summary | limitTo : 1024 $}
                        <span ng-if="entity.description.text.length > 1024">...</span>
                    </p>
                    
                    <!--Events-->
                    <p ng-if="entity.description.text">
                        {$ entity.description.text || limitTo : 1024 $}
                        <span ng-if="entity.description.text.length > 1024">...</span>
                    </p>
                    
                    <!--Projects-->
                    <p ng-if="entity.description && !entity.description.text">
                        {$ entity.description || limitTo : 1024 $}
                        <span ng-if="entity.description.length > 1024">...</span>
                    </p>
                    
                    <!--link to source-->
                    <p ng-if="!preview && (entity.link || entity.source)" class="text-red">
                        <a href="{$ entity.link || entity.url $}" target="_blank">Got to source</a>
                    </p>
                
                </div>

                
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
        controller : ['$scope', function($scope) {}]
    }
}]



