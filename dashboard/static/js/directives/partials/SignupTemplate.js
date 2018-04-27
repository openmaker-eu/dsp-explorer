
let templates= {
    select:`
        <select name="{$ name $}" id="" class="form-control">
            <option ng-repeat="dato in data track by $index" value="{$ dato.value $}">{$ dato.label $}</option>
        </select>
    `,
    text : `<input name="{$ name $}" type="text" value="{$ data $}" class="form-control">
    `,
    slider :`<input name="{$ name $}" type="range" min="0" max="100" value="{$ data $}" class="form-control">`,
    login : `
        <label class="signup-template__label" for="email">email</label>
        <input name="email" type="email" value="{$ data $}" class="form-control"><br>
        <label class="signup-template__label" for="password">password</label>
        <input name="password" type="password" value="{$ data $}" class="form-control"><br>
        <label class="signup-template__label" for="password_confirm">repeat password</label>
        <input name="password_confirm" type="password" value="{$ data $}" class="form-control"><br>
    `,
    close :`<h1 class="signup-template__label text-brown">
        <i class="fa fa-check-circle-o" style=" font-size:400%; font-weight:300;"><i><br>
        <h1 class="signup-template__label">Check your inbox for a confirmation email</h1>
    </h1>`,
    date: `
        <input class="form-control"
        ng-model="data"
        format="YYYY-MM-DD"
        ng-model-options="{updateOn:'blur'}"
        placeholder="Select a date..."
        moment-picker="data">
    `,
    multi_select: `
        <div>
            <ui-select
                multiple tagging
                tagging-label="" tagging-tokens="SPACE|ENTER|,|/|<|>|{|}|^"
                sortable="true"
                spinner-enabled="true"
                class="form-control"
                ng-model="tags"
                title="Choose a tag" limit="3"
            >
                <ui-select-match placeholder="Type a tag and press enter *">{$ $item $}</ui-select-match>
                <ui-select-choices repeat="tag in data | filter:$select.search track by $index">
                    <div ng-bind-html="tag | highlight: $select.search"></div>
                </ui-select-choices>
            </ui-select><br/>
            <input type="hidden" name="{$ name $}" ng-value="tags" required/>
        </div>
    `,
    city: `
        <input ng-init="place={};"
             autocomplete="**********"
             required
             class="form-control"
            
             vs-google-autocomplete="{ types:['(cities)'] }"
             vs-autocomplete-validator
             ng-model="city"
             vs-latitude ="place.lat"
             vs-longitude="place.long"
             vs-street-number="place.street_number"
             vs-street="place.street"
             vs-city="place.city"
             vs-state="place.state"
             vs-country="place.country"
             vs-country-short="place.country_short"
             vs-post-code="place.post_code"
            
             type="text" name="city" id="city"
             placeholder="Start typing the city name where you are based *"><br />
            
        <input type="hidden" value="{$ place $}" name="place">
    `
}

export default ['$compile', function($compile){
    return {
        template:`
             <div class="signup-template">
                <div class="" style="padding:5%;">
                    <h1 class="signup-template__label">{$ label $}</h1>
                    <br>
                    <div class="signup-input"></div>
                </div>
            <div>
        `,
        scope: {
            type : '@',
            data : '=',
            label : '@'
        },
        link: function($scope, $element, $attr){
            $element.find('.signup-input').html($compile(templates[$attr.type])($scope))
        },
        controller : ['$scope',function($scope){
            $scope.tags = []
            $scope.$watch('data', (a, b)=>console.log('async', a,b))
    
        }]
    }
}]
