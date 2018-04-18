export default [function(){
    return {
        template:`
            <div class="om-spinner">
                  <div class="om-spinner__bounce1 om-spinner__bounce"></div>
                  <div class="om-spinner__bounce2 om-spinner__bounce"></div>
                  <div class="om-spinner__bounce3 om-spinner__bounce"></div>
            </div>
            
            <style>
            
            .om-spinner {
              /*margin: 100px auto 0;*/
              margin: 0 auto;
              width: 70px;
              text-align: center;
            }
            
            .om-spinner > div {
              width: 18px;
              height: 18px;
              background-color: #333;
            
              border-radius: 100%;
              display: inline-block;
              -webkit-animation: sk-om-spinner__bouncedelay 1.4s infinite ease-in-out both;
              animation: sk-om-spinner__bouncedelay 1.4s infinite ease-in-out both;
            }
            
            .om-spinner .om-spinner__bounce1 {
              -webkit-animation-delay: -0.32s;
              animation-delay: -0.32s;
            }
            
            .om-spinner .om-spinner__bounce2 {
              -webkit-animation-delay: -0.16s;
              animation-delay: -0.16s;
            }
            
            @-webkit-keyframes sk-om-spinner__bouncedelay {
              0%, 80%, 100% { -webkit-transform: scale(0) }
              40% { -webkit-transform: scale(1.0) }
            }
            
            @keyframes sk-om-spinner__bouncedelay {
              0%, 80%, 100% {
                -webkit-transform: scale(0);
                transform: scale(0);
              } 40% {
                -webkit-transform: scale(1.0);
                transform: scale(1.0);
              }
            }
            </style>
            
        `,
        scope: {
            entityname : '@',
            entityid : '@'
        },
        controller : ['$scope', '$http', '$rootScope', function($scope, $http, $rootScope){
            $scope.interested = false;
            // $scope.interest = (challenge) => $scope.interested = !$scope.interested
    
            // Build url
            let url = `/api/v1.4/interest/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                if(res.status === 200){
                    $scope.interested = _.get(res, 'data.result.iaminterested', $scope.interested)
                    $rootScope.$emit('interested.new')
                }
            }
    
            // First check if is bookmarked
            $http.get(url).then(change_status)
    
            // Change bookmark on BE
            $scope.interest = () =>{ $http.post(url).then(change_status) }
            
        }]
    }
}]
