{% extends "layout.html" %}
{% block body %}

{% if current_user.is_authenticated() %}

    <div class="row">
        <div class=" small-12 columns">
          <h4>Your Links</h4>
        </div>
    </div>
    <ul class="pagination">
    {% for link in links %}
      <div class="row">
        <div class=" small-10 columns">
            <strong> {{link.title}}:</strong>
             <a href="/urly/{{ link.short }}" target="_blank">
               /urly/{{ link.short }}</a>
            {% if link.description %}
               <br>{{ link.description }}
            {% endif %}
            <div class="row">
            <form method="POST" action="{{ url_for("delete_link") }}">
              <input type="hidden" name="link_id" value="{{ link.id }}"/>
              <input type="submit" class="submitlink" value="Delete Link "/>
            </form><a class="button tiny" href="{{ url_for("update_link", id=link.id) }}">   Update Link</a>
          </div>
            <div class="row">
             <hr>
            </div>
    {% endfor %}
    </ul>
  {% else %}
  <div class="row">
     <div class=" small-12 columns">
        <ul class="example-orbit" data-orbit>
          <img src="{{ url_for('static', filename='dogs1.png') }}" alt="slide 1" />
      </div>
  </div>
  <div class="row">
       <div class="small-1 columns"></div>
       <div class="small-11 columns"><h2> Ana's URL Shortener - Small is the New Big</h2></div>
  </div>


{% endif %}



{% endblock %}
