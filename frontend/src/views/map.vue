<template>
  <div>
    <div style="margin:10px">
      请输入:
      <input id="suggestId" type="text" size="30" style="width:300px" />
    </div>
    <div class="lng-lat">
      <div class="item">
        当前经度:
        <input v-model="lng" />
      </div>
      <div class="item">
        当前纬度:
        <input v-model="lat" />
      </div>
    </div>
    <!-- <div id="searchResultPanel"></div> -->
    <div id="container" style="width: 600px; height: 400px;"></div>
  </div>
</template>

<script>
export default {
  name: "BaiduMap",
  data() {
    return {
      map: null,
      myValue: "",
      lng: "",
      lat: "",
    };
  },
  mounted() {
    this.loadBaiduMap(() => {
      this.initMap();
    });
  },
  methods: {
    loadBaiduMap(callback) {
      if (typeof BMap !== "undefined") {
        callback();
        return;
      }

      const script = document.createElement("script");
      script.type = "text/javascript";
      script.src =
        "http://api.map.baidu.com/api?v=2.0&ak=mK5CDIAi1mk8Le8z3RCTto1KLzGCG0hQ&callback=initBMap";
      document.head.appendChild(script);

      window.initBMap = () => {
        callback();
      };
    },
    initMap() {
      this.map = new BMap.Map("container");
      const centerPoint = new BMap.Point(116.3964, 39.9093);
      this.map.centerAndZoom(centerPoint, 13);
      this.map.enableScrollWheelZoom();

      const ac = new BMap.Autocomplete({
        input: "suggestId",
        location: this.map,
      });

      ac.addEventListener("onconfirm", (e) => {
        const _value = e.item.value;
        this.myValue =
          _value.province +
          _value.city +
          _value.district +
          _value.street +
          _value.business;

        this.setPlace();
      });

      this.map.addEventListener("click", (e) => {
        this.lng = e.point.lng.toFixed(6);
        this.lat = e.point.lat.toFixed(6);
        this.addMarker(new BMap.Point(e.point.lng, e.point.lat));
      });
    },
    setPlace() {
      const myGeo = new BMap.Geocoder();
      myGeo.getPoint(this.myValue, (point) => {
        if (point) {
          this.map.centerAndZoom(point, 16);
          this.addMarker(point);
        }
      }, "北京");
    },
    addMarker(point) {
      this.clearMarkers();
      const marker = new BMap.Marker(point);
      this.map.addOverlay(marker);
    },
    clearMarkers() {
      const allOverlay = this.map.getOverlays();
      for (let i = 0; i < allOverlay.length - 1; i++) {
        this.map.removeOverlay(allOverlay[i]);
      }
    },
  },
};
</script>

<style scoped>
.lng-lat {
  margin: 0 0 30px 0px;
}
.lng-lat .item {
  margin: 10px;
}
#searchResultPanel {
  border: 1px solid #C0C0C0;
  width: 300px;
  height: 600px;
  position: absolute;
  left: 650px;
  top: 20px;
}
</style>
