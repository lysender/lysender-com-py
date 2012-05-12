/** 
 * CookieGroup class definition
 *
 * Compared to the PHP version, CookieGroup JavaScript version
 * does not use expire parameter in UNIX timestamp,
 * instead, it is the number of seconds relative to current time.
 *
 */
function CookieGroup(name, expire, path, domain) {
    this.init(name, expire, path, domain);
}

CookieGroup.prototype = {
    STATUS_MISSING: 'missing',
    STATUS_INVALID: 'invalid',
    STATUS_OK: 'ok',

    status: null,
    value: {},

    name: null,
    expire: 0,
    path: '/',
    domain: null,

    init: function(name, expire, path, domain) {
        this.name = name;
        this.expire = expire;
        this.path = path;
        this.domain = domain;
    },

    _getTimestamp: function() {
        return Math.round((new Date()).getTime() / 1000);
    },

    _getExpiresTimestamp: function() {
        if (this.expire > 0) {
            return this._getTimestamp() + this.expire;
        } else {
            return 0;
        }
    },

    setValue: function(name, value) {
        this.value[name] = [value, this._getExpiresTimestamp()];

        return this;
    },

    getValue: function(name) {
        if (name in this.value) {
            var v = this.value[name];

            // Check if value and expiry exists and does not yet expires except for session cookies
            if (typeof v[0] !== "undefined" && typeof v[1] !== "undefined") {
                var expire = parseInt(v[1]);

                if (!isNaN(expire)) {
                    if (expire === 0 || this._getTimestamp() < expire) {
                        return v[0];
                    }
                }
            }
        }

        return null;
    },

    removeValue: function(name) {
        if (name in this.value) {
            delete this.value[name];
        }

        return this;
    },

    toJSONString: function() {
        var ret = JSON.stringify(this.value);

        if (ret) {
            return ret;
        }

        return null;
    },

    getStatus: function() {
        return this.status;
    },

    fetchGroup: function() {
        var cookie = this.getCookie(this.name);
        var c = null;

        if (cookie) {
            try {
                c = JSON.parse(cookie);
            } catch (e) {
                c = null;
            }

            if (c && typeof c === "object") {
                this._loadValues(c);
                this.status = this.STATUS_OK;
            } else {
                this.status = this.STATUS_INVALID;
            }
        } else {
            this.status = this.STATUS_MISSING;
        }
        
        return this.status;
    },

    _loadValues: function(data) {
        // Clear values first
        this.value = {};

        if (typeof data == "object") {
            for (var name in data) {
                var v = data[name];

                if (typeof v[0] !== "undefined" && typeof v[1] !== "undefined") {
                    var expire = parseInt(v[1]);

                    if (!isNaN(expire)) {
                        if (expire === 0 || this._getTimestamp() < expire) {
                            this.value[name] = [v[0], v[1]];
                        }
                    }
                }
            }
        }

        return this;
    },

    writeGroup: function() {
        this.setCookie(this.name, this.toJSONString(), this.expire, this.path, this.domain);

        return this;
    },

    removeGroup: function() {
        this.setCookie(this.name, '', 86400, this.path);

        return this;
    },

    getCookie: function(name) {
        var results = document.cookie.match(name + '=(.*?)(;|$)');

        if (results) {
            return (unescape(results[1]));
        }

        return null;
    },

    setCookie: function(name, value, expire, path, domain) {
        if (expire === 0) {
            document.cookie = name + "=" + value + "; path=" + path + "; domain=" + domain;
        } else {
            var date = new Date();
            date.setTime(date.getTime() + (expire*1000));
            var e = "; expires=" + date.toGMTString();
            document.cookie = name + "=" + value + e + "; path=" + path + "; domain=" + domain;
        }
    }
};

window.CookieGroupHandler = {
    config: {
        'lys10years': {
            'expire': 315360000,
            'path': '/'
        },
        'lyssession': {
            'expire': 0,
            'path': '/'
        }
    },

    instances: {},

    getCookieInstance: function(name) {
        if (name in this.config) {
            if (name in this.instances) {
                return this.instances[name];
            } else {
                this.instances[name] = new CookieGroup(name, this.config[name]['expire'], this.config[name]['path'], window.location.hostname);
                this.instances[name].fetchGroup();

                return this.instances[name];
            }
        }
    }
};

/** 
* Sample usage below
(function(){
    $(function(){
        cg = new CookieGroup('lys30days', 2592000, '/', window.location.hostname);
        cg.fetchGroup();
        //cg.setValue('atcdate', '2011-12-21');
        //cg.setValue('checkoutdate', '2011-12-25');
        //cg.setValue('bannerclosed', '1');
        console.log(cg.getValue('atcdate'));
        console.log(cg.getValue('bannerclosed'));
        cg.writeGroup();

        cg2 = new CookieGroup('lyssession', 0, '/', window.location.hostname);
        cg2.fetchGroup();
        //cg2.setValue('isCheckout', 1);
        //cg2.setValue('event', 'scCheckout');
        //cg2.setValue('isKairos', 1);
        //cg2.setValue('isScene7', 1);
        //cg2.setValue('isIs', 1);
        console.log(cg2.getValue('event'));
        cg2.writeGroup();

        cg3 = new CookieGroup('lys45days', 3888000, '/', window.location.hostname);
        cg3.fetchGroup();
        //cg3.setValue('ORDERID', '123456');
        //cg3.setValue('SHOPPERID', '14344');
        //cg3.setValue('isBongo', '1');
        console.log(cg3.value);
        console.log(cg3.getValue('ORDERID'));
        console.log(cg3.getValue('SHOPPERID'));
        console.log(cg3.getValue('isBongo'));
        cg3.writeGroup();
    });
})(jQuery);
*/