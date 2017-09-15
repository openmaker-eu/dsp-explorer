import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <a ng-href="{$ href $}" ng-class="{ 'not-pointer': !href }" style="display: block;">
        <div class="profile-image-static" style="border-radius:50%; overflow: hidden; z-index:1000;">
            <img ng-src="{$ src $}" style="width:100%; height:100%; position: absolute;  "/>
        </div>
    </a>
    <style>
        .not-pointer , .not-pointer *{ cursor:default!important; }
    </style>
    &nbsp;&nbsp;&nbsp;&nbsp;
`

export default [function(){
    
    return {
        template:template,
        scope : {
            src : '=',
            href : '='
        },
        link : function($scope, element, attrs){

            $(element).css({display:'block'})
            
            $scope.fitImageToCircle = (image)=> {
        
                if( !image || !image.get(0) ) return
                image.removeAttr('style')
        
                let width = image.get(0).naturalWidth
                let height = image.get(0).naturalHeight
                let css = {'display':'block', 'position': 'absolute'}
                width > height? css.height = '100%' : css.width = '100%'
                image.css({ display:'block'})
                image.css(css)
        
            }
            
            let img = element.find('img');
            img.bind('load', n=>$scope.fitImageToCircle($(img)))
        }
    }
    
}]