module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        cssmin: {
            css: {
                banner: "/* <%= pkg.name %> <%= pkg.version %> */",
                files: {
                    'media/release/<%= pkg.name %>.min.css': [
                        'media/src/css/*.css',
                        'media/build/css/*.css'
                    ]
                }
            }
        },
        less: {
            'media/build/css/styles.css': 'media/src/less/styles.less'
        },
        watch: {
            statics: {
                files: [
                    'package.json', 
                    'media/**/*.js', 
                    'media/**/*.less',
                    'media/**/*.css', 
                    '!**/*.min.js', 
                    '!**/*.min.css'],
                tasks: ['build']
            }
        },
        uglify: {
            js: {
                files: {
                    'media/release/<%= pkg.name %>.min.js': [
                        'media/src/js/jquery.js',
                        'media/src/js/*.js'
                    ]
                }
            }
        },
        clean: ['media/build', 'media/release']
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');

    grunt.registerTask('default', ['build', 'watch']);
    grunt.registerTask('build', ['clean', 'less', 'cssmin', 'uglify']);
};
