jQuery(function ($) {

    var MyMainAPP = window.MyMainAPP || {};

    /* ==================================================
       Mobile Navigation
    ================================================== */
    var mobileMenuClone = $('#menu').clone().attr('id', 'navigation-mobile');

    MyMainAPP.mobileNav = function () {
        var windowWidth = $(window).width();

        if (windowWidth <= 979) {
            if ($('#mobile-nav').length > 0) {
                mobileMenuClone.insertAfter('#menu');
                $('#navigation-mobile #menu-nav').attr('id', 'menu-nav-mobile');
            }
        } else {
            $('#navigation-mobile').css('display', 'none');
            if ($('#mobile-nav').hasClass('open')) {
                $('#mobile-nav').removeClass('open');
            }
        }
    };

    MyMainAPP.listenerMenu = function () {
        $('#mobile-nav').on('click', function (e) {
            $(this).toggleClass('open');

            if ($('#mobile-nav').hasClass('open')) {
                $('#navigation-mobile').slideDown(500, 'easeOutExpo');
            } else {
                $('#navigation-mobile').slideUp(500, 'easeOutExpo');
            }
            e.preventDefault();
        });

        $('#menu-nav-mobile a').on('click', function () {
            $('#mobile-nav').removeClass('open');
            $('#navigation-mobile').slideUp(350, 'easeOutExpo');
        });
    };


    /* ==================================================
       Slider Options
    ================================================== */


    /* ==================================================
       Navigation Fix
    ================================================== */

    MyMainAPP.nav = function () {
        $('.sticky-nav').waypoint('sticky');
    };


    /* ==================================================
       Filter Works
    ================================================== */

    MyMainAPP.filter = function () {
        if ($('#projects').length > 0) {
            var $container = $('#projects');

            $container.imagesLoaded(function () {
                $container.isotope({
                    // options
                    animationEngine: 'best-available',
                    itemSelector: '.item-thumbs',
                    layoutMode: 'fitRows'
                });
            });


            // filter items when filter link is clicked
            var $optionSets = $('#options .option-set'),
                $optionLinks = $optionSets.find('a');

            $optionLinks.click(function () {
                var $this = $(this);
                // don't proceed if already selected
                if ($this.hasClass('selected')) {
                    return false;
                }
                var $optionSet = $this.parents('.option-set');
                $optionSet.find('.selected').removeClass('selected');
                $this.addClass('selected');

                // make option object dynamically, i.e. { filter: '.my-filter-class' }
                var options = {},
                    key = $optionSet.attr('data-option-key'),
                    value = $this.attr('data-option-value');
                // parse 'false' as false boolean
                value = value === 'false' ? false : value;
                options[key] = value;
                if (key === 'layoutMode' && typeof changeLayoutMode === 'function') {
                    // changes in layout modes need extra logic
                    changeLayoutMode($this, options)
                } else {
                    // otherwise, apply new options
                    $container.isotope(options);
                }

                return false;
            });
        }
    };


    /* ==================================================
       FancyBox
    ================================================== */

    MyMainAPP.fancyBox = function () {
        if ($('.fancybox').length > 0 || $('.fancybox-media').length > 0 || $('.fancybox-various').length > 0) {

            $(".fancybox").fancybox({
                padding: 0,
                beforeShow: function () {
                    this.title = $(this.element).attr('title');
                    this.title = '<h4>' + this.title + '</h4>' + '<p>' + $(this.element).parent().find('img').attr('alt') + '</p>';
                },
                helpers: {
                    title: {type: 'inside'},
                }
            });

            $('.fancybox-media').fancybox({
                openEffect: 'none',
                closeEffect: 'none',
                helpers: {
                    media: {}
                }
            });
        }
    };


    /* ==================================================
       Contact Form
    ================================================== */

    MyMainAPP.contactForm = function () {
        $("#contact-submit").on('click', function () {
            $contact_form = $('#contact-form');

            var fields = $contact_form.serialize();

            $.ajax({
                type: "POST",
                url: "/static/php/contact.php",
                data: fields,
                dataType: 'json',
                success: function (response) {

                    if (response.status) {
                        $('#contact-form input').val('');
                        $('#contact-form textarea').val('');
                    }

                    $('#response').empty().html(response.html);
                }
            });
            return false;
        });
    };


    /* ==================================================
       Twitter Feed
    ================================================== */

    MyMainAPP.tweetFeed = function () {

        var valueTop = -64; // Margin Top Value

        $("#ticker").tweet({
            modpath: '/static/js/twitter/',
            username: "Bluxart", // Change this with YOUR ID
            page: 1,
            avatar_size: 0,
            count: 10,
            template: "{text}{time}",
            filter: function (t) {
                return !/^@\w+/.test(t.tweet_raw_text);
            },
            loading_text: "loading ..."
        }).bind("loaded", function () {
            var ul = $(this).find(".tweet_list");
            var ticker = function () {
                setTimeout(function () {
                    ul.find('li:first').animate({marginTop: valueTop + 'px'}, 500, 'linear', function () {
                        $(this).detach().appendTo(ul).removeAttr('style');
                    });
                    ticker();
                }, 5000);
            };
            ticker();
        });

    };


    /* ==================================================
       Next Section
    ================================================== */

    MyMainAPP.goSection = function () {
        $('#nextsection').on('click', function () {
            $target = $($(this).attr('href')).offset().top - 30;

            $('body, html').animate({scrollTop: $target}, 750, 'easeOutExpo');
            return false;
        });
    };

    /* ==================================================
       GoUp
    ================================================== */

    MyMainAPP.goUp = function () {
        $('#goUp').on('click', function () {
            $target = $($(this).attr('href')).offset().top - 30;

            $('body, html').animate({scrollTop: $target}, 750, 'easeOutExpo');
            return false;
        });
    };


    /* ==================================================
        Scroll to Top
    ================================================== */

    MyMainAPP.scrollToTop = function () {
        var windowWidth = $(window).width(),
            didScroll = false;

        var $arrow = $('#back-to-top');

        $arrow.click(function (e) {
            $('body,html').animate({scrollTop: "0"}, 750, 'easeOutExpo');
            e.preventDefault();
        })

        $(window).scroll(function () {
            didScroll = true;
        });

        setInterval(function () {
            if (didScroll) {
                didScroll = false;

                if ($(window).scrollTop() > 1000) {
                    $arrow.css('display', 'block');
                } else {
                    $arrow.css('display', 'none');
                }
            }
        }, 250);
    };

    /* ==================================================
       Thumbs / Social Effects
    ================================================== */

    MyMainAPP.utils = function () {

        $('.item-thumbs').bind('touchstart', function () {
            $(".active").removeClass("active");
            $(this).addClass('active');
        });

        $('.image-wrap').bind('touchstart', function () {
            $(".active").removeClass("active");
            $(this).addClass('active');
        });

        $('#social ul li').bind('touchstart', function () {
            $(".active").removeClass("active");
            $(this).addClass('active');
        });

    };

    /* ==================================================
       Accordion
    ================================================== */

    MyMainAPP.accordion = function () {
        var accordion_trigger = $('.accordion-heading.accordionize');

        accordion_trigger.delegate('.accordion-toggle', 'click', function (event) {
            if ($(this).hasClass('active')) {
                $(this).removeClass('active');
                $(this).addClass('inactive');
            }
            else {
                accordion_trigger.find('.active').addClass('inactive');
                accordion_trigger.find('.active').removeClass('active');
                $(this).removeClass('inactive');
                $(this).addClass('active');
            }
            event.preventDefault();
        });
    };

    /* ==================================================
       Toggle
    ================================================== */

    MyMainAPP.toggle = function () {
        var accordion_trigger_toggle = $('.accordion-heading.togglize');

        accordion_trigger_toggle.delegate('.accordion-toggle', 'click', function (event) {
            if ($(this).hasClass('active')) {
                $(this).removeClass('active');
                $(this).addClass('inactive');
            }
            else {
                $(this).removeClass('inactive');
                $(this).addClass('active');
            }
            event.preventDefault();
        });
    };

    /* ==================================================
       Tooltip
    ================================================== */

    MyMainAPP.toolTip = function () {
        $('a[data-toggle=tooltip]').tooltip();
    };


    /* ==================================================
        Init
    ================================================== */

    $(document).ready(function () {

        // Get the modal_container
        var modal_container = document.getElementById('id_modal_container');
        var modal_img = document.getElementById("id_modal_img");
        var modal_caption = document.getElementById("id_modal_caption");

        $('.item_img_thumb').onclick = function () {
            modal_container.style.display = "block";
            modal_img.src = this.src;
            modal_caption.innerHTML = this.alt;
        };

        // Get the <modal_span> element that closes the modal_container
        var modal_span = document.getElementsByClassName("modal_close")[0];

        // When the user clicks on <modal_span> (x), close the modal_container
        modal_span.onclick = function () {
            modal_container.style.display = "none";
        }
    });

    $(window).resize(function () {
        MyMainAPP.mobileNav();
    });

});
