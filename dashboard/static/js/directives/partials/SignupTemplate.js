
let templates= {
    ddl:`
        <select name="" id="" class="form-control">
            <option ng-repeat="dat in data track by $index" value="">{$ dat $}</option>
        </select>
    `,
    text : `
       <input type="text" value="{$ data $}" class="form-control">

    `,
    slider :`
        <input type="range" min="0" max="100" value="{$ data $}" class="form-control">
    `,
    close :`
        <h1 class="signup-template__label text-brown"><i class="fa fa-check-circle-o" style=" font-size:400%;"><i></h1>
    `
    
}

export default ['$compile', function($compile){
    return {
        template:`
             <div class="signup-template">
                <div class="">
                    <h1 class="signup-template__label">{$ label $}</h1>
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
            
            console.log($scope);
            console.log($compile(templates[$attr.type])($scope));
    
            $element.find('.signup-input').html($compile(templates[$attr.type])($scope))

        },
        controller : ['$scope',function($scope){
            console.log('keeiii');
        }]
    }
}]
