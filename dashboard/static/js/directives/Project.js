import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div class="col-md-12">
        <div class="form-group">
            <div class="col-md-12">
                <label style="width:100%; text-align: center;">Project Image</label>
            </div>
            <div class="col-lg-4 col-lg-offset-4 col-md-6 col-md-offset-3 col-xs-6 col-xs-offset-3 text-center" >

                <button class="btn custom-button margin-bottom-10" ng-click="profileImageUpload();">Image</button>

                <div ng-if="image_model.src" class="thumbnail" id="profile-image-div" >
                    <img ng-src="{$ image_model.src $}"/>
                </div>

                <input
                        id="profile-image-input"
                        class="hidden"
                        input_file_model="image_model.src"
                        type="file"
                        name="profile_img"/>
            </div>
        </div>
        <div class="form-group">
            <div class="col-md-12">
                <label>Project name</label>
                <input type="text" class="form-control" id="project_name" placeholder="Insert project name">
            </div>
        </div>
        <div class="form-group">
            <div class="col-md-12">
                <label>Description</label>
                <textarea type="text" rows="10" class="form-control" id="description" placeholder="Insert a description"></textarea>
            </div>
        </div>
        <div class="form-group">
            <div class="col-md-6">
                <label>Start date</label>
                <input type="date"/ ng-model="start_date">
            </div>
            <div ng-if="!ongoing" class="col-md-6">
                <label>Start date</label>
                <input type="date"/ ng-model="end_date">
            </div>
            <div class="col-md-12">
                <label>Ongoing</label>
                <input type="checkbox" aria-label="Ongoing" ng-model="ongoing">
            </div>
        </div>
        <div class="form-group">
            <div class="col-md-12">
                <label>Your role</label>
                <input type="text" class="form-control" id="role" placeholder="Insert your role"/>
            </div>
        </div>

        <div class="form-group">
            <div class="col-md-12">
                <label>Project url</label>
                <input type="text" class="form-control" id="project_url" placeholder="Insert your project url"/>
            </div>
        </div>
        <div class="form-group">
            <div class="col-md-12">
                <label>Tags</label>
                <div>
                <ui-select
                           multiple tagging
                           tagging-label="" tagging-tokens="SPACE|ENTER|,|/|<|>|{|}|^"
                           sortable="true"
                           spinner-enabled="true"
                           ng-class="{'form-control':true}"
                           ng-model="av_tags.selected"
                           title="Choose a tag *" limit="5"
                >

                    <ui-select-match placeholder="Type a tag and press enter *">
                        {$ $item $}
                    </ui-select-match>

                    <ui-select-choices repeat="tag in av_tags.available | filter:$select.search track by $index">
                        <div ng-bind-html="tag | highlight: $select.search"></div>
                    </ui-select-choices>

                </ui-select><br/>

                <input type="hidden" name="tags" ng-value="av_tags.selected" required/>

            </div>
        </div>
    </div>
`

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', tags: '=' },
        controller : ['$scope', '$http', '$sce', function($scope, $http, $sce){
        console.log("project controller")
        $scope.profileImageUpload = n=>$('#profile-image-input').trigger('click')
        $scope.av_tags={ available:  $scope.tags  }
            /*$scope.get_data = ()=> Promise
                    .all([
                        $http.get('/api/v1.3/challenge/'+$scope.id+'/'),
                        $http.get('/api/v1.3/interest_ids/')
                    ])
                    .then(
                        res=>{
                            res[0].data.details = res[0].data.details && $sce.trustAsHtml(res[0].data.details)
                            $scope.challenge = res[0].data || {}
                            $scope.interested_ids = res[1].data || []
                            $scope.$apply(()=>$(window).trigger('resize'))
                        },
                        err=>console.log('Error: ', err)
                    )
    
            $scope.get_data()
            
            $scope.click_interest = (challenge) =>
                ($scope.is_interested(challenge) ?
                    $http.delete('/api/v1.3/interest/challenge/'+challenge.id+'/') :
                    $http.post('/api/v1.3/interest/challenge/'+challenge.id+'/')
                )
                .then(res=>$scope.get_data(),err=>console.log(err))
            
            $scope.is_interested = (challenge)=>$scope.interested_ids && $scope.interested_ids.indexOf(challenge.id) > -1
            */
 
        }]
    }
}]



