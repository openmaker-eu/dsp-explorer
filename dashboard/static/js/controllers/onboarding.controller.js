/**
 * Created by andreafspeziale on 06/07/17.
 */
export default [ '$scope','$http', function ($scope, $http) {

    console.log('onboarding controller')

    $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(),
        startingDay: 1,
    };

    $scope.datePopup = {
        opened: false
    };

    $scope.openDatePopUp = function() {
        $scope.datePopup.opened = true;
    };

    $scope.profileImageUpload = () => {
        $('#profile-image-input').trigger('click')
    }

    $scope.previewImage = (input) => {

        if (input.files && input.files[0]) {
            
            var reader = new FileReader();
            
            reader.onload = (e) => {
    
                let image = $('#profile-image');
                
                image.removeAttr('style');
                
                image.on('load', ()=>{
                    
                    let width = image.get(0).naturalWidth
                    let height = image.get(0).naturalHeight
                    
                    let css = {'display':'block', 'position': 'absolute'}
                    width > height? css.height = '100%' : css.width = '100%'
                    image.css(css);
                    
                })
                
                image.attr('src', e.target.result)
    
            }
            reader.readAsDataURL(input.files[0]);
            
        }
    }

}]