export default function(){
    return {
        template:`
            <div>
                <!--Loading Data-->
                <div ng-if="loading" class="text-center">
                    <h4>
                        <span ng-if="!custommessage">Loading <span class="capitalize">{$ entityname $}</span></span>
                        <span ng-if="custommessage" >{$ custommessage $}</span>
                        <br><br>
                        
                        <div class="om-spinner">
                            <div class="om-spinner__bounce1 om-spinner__bounce"></div>
                            <div class="om-spinner__bounce2 om-spinner__bounce"></div>
                            <div class="om-spinner__bounce3 om-spinner__bounce"></div>
                        </div>
                        
                    </h4>
                    <br>
                </div>
                <!--No data-->
                <div ng-if="error" style="padding:5%;">
                    <h4>
                        <span ng-if="!errormessage">There are no <span class="capitalize">{$ entityname $}</span> available</span>
                        <span ng-if="errormessage">{$ errormessage $}</span>
                    </h4>
                </div>

            </div>
        `,
        scope: {
            loading : '=',
            error : '=',
            entityname : '@',
            errormessage : '@',
            custommessage : '@'
        },
        controller : ['$scope', '$rootScope', function($scope, $rootScope){
        }]
    }
}
