
let templates= {
    ddl:`
        <select name="name" id="" class="form-control">
            <option ng-repeat="dato in data track by $index" value="{$ dato.value $}">{$ dato.label $}</option>
        </select>
    `,
    text : `
       <input name="name" type="text" value="{$ data $}" class="form-control">

    `,
    slider :`
        <input name="name" type="range" min="0" max="100" value="{$ data $}" class="form-control">
    `,
    login : `
        <label class="class="signup-template__label"" for="email">email</label>
        <input name="email" type="password" value="{$ data $}" class="form-control"><br>
        <label class="class="signup-template__label"" for="password">password</label>
        <input name="password" type="password" value="{$ data $}" class="form-control"><br>
        <label class="class="signup-template__label"" for="password_confirm">repeat password</label>
        <input name="password_confirm" type="password" value="{$ data $}" class="form-control"><br>
    `,
    close :`
        <h1 class="signup-template__label text-brown"><i class="fa fa-check-circle-o" style=" font-size:400%;"><i></h1>
    `
    
}

export default ['$compile', function($compile){
    return {
        template:`
             <div class="signup-template">
                <div class="" style="padding:5%;">
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
