<!DOCTYPE html>
<html>
    <head>
        <title>
            <%block name='title'>
                ${view.igniter.brand}
                % if view.name != view.igniter.brand:
                    - ${view.name}
                % endif
            </%block>
        </title>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <%block name='head'>
        <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.min.css'>
        </%block>
        <%block name='head_tail'/>
    </head>
    <body>
        <div class='wrap'>
        <%block name='page_body'>
        <div class='container'>
        <div class='<%block name='navbar_class'>navbar navbar-default</%block>' role='navigation'>
            <div class='container'>            
                <div class='navbar-header'>
                    <%block name='brand'><a href='${view.igniter.url}' class='navbar-brand'>${view.igniter.brand}</a></%block>
                </div>
                <div class='collapse navbar-collapse'>
                    <ul class="nav navbar-nav">
                    % for item in view.igniter.menu:
                        % if not item['url']:
                            <li class='dropdown'>
                                <a class='dropdown-toggle' data-toggle='dropdown' href='javascript:void(0)'>${item['name']}<b class='caret'></b></a>
                                <ul class='dropdown-menu'>
                                    % for child in view.igniter.menu_categories[item['name']]:
                                        <li><a href='${child['url']}'>${child['name']}</a></li>
                                    % endfor
                                </ul>
                            </li>
                        % else:
                            <li${" class='active'" if view.igniter.is_active(request, item) else '' | n}><a href='${item['url']}'>${item['name']}</a></li>
                        % endif
                    % endfor
                    </ul>
                    <ul class='nav navbar-nav navbar-right'>
                        <%block name='menu_links'/>
                    </ul>
                </div>
            </div>
        </div>
        </div>
        </%block>

        <div class='container'>
            <%block name='content'/>
        </div>
        </div> <!-- /wrap -->

        <%block name='footer'>
        % if view.igniter.footer:
        <div class='footer'>
            <div class='container'>
                <div class='collapse navbar-collapse'>
                    % for item in view.igniter.footer:
                        <div class='${view.igniter.footer_class}''>
                        % if not item['url']:
                            <h4 class='footer_category'>${item['name']}</h4>
                            <ul>
                            % for child in view.igniter.footer_categories[item['name']]:
                                <li><a href='${child['url']}'>${child['name']}</a></li>
                            % endfor
                            </ul>
                        % else:
                            <a href='${item['url']}'>${item['name']}</a>
                        % endif
                        </div>
                    % endfor
                    <%block name='footer_tail'/>
                </div>
            </div>
        </div>
        % endif
        </%block>

        <%block name='tail_js'>
        <script type='text/javascript' src='//code.jquery.com/jquery-1.11.0.min.js'></script>
        <script type='text/javascript' src='//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.min.js'></script>
        </%block>
        <%block name='tail'/>
    </body>
</html>
