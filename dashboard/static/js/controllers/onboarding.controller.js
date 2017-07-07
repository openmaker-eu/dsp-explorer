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
                $('#profile-image').attr('src', e.target.result).css( {
                    'max-width':'150%',
                    'min-width': '100%',
                    'min-height':'100%',
                    'max-height':'150%',
                    'display':'block',
                    'position': 'absolute'});
            }

            reader.readAsDataURL(input.files[0]);
        }
    }

}]