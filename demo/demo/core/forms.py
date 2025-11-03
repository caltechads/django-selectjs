from book_manager.models import Author, Binding, Book, Publisher
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    ButtonHolder,
    Field,
    Fieldset,
    Layout,
    Submit,
)
from django import forms
from django.urls import reverse
from selectjs.widgets import (
    ModelM2MSearchSelectWidget,
    ModelSearchSelectWidget,
)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "binding", "publisher", "authors"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up ModelSearchSelectWidget for binding field
        self.fields["binding"].widget = ModelSearchSelectWidget(
            model=Binding,
            search_field="name",
            api_endpoint=reverse("async_select_search"),
        )
        self.fields["authors"].widget = ModelM2MSearchSelectWidget(
            model=Author,
            search_field="full_name",
            api_endpoint=reverse("async_select_search"),
        )
        # Set up ModelSearchSelectWidget for publisher field
        self.fields["publisher"].widget = ModelSearchSelectWidget(
            model=Publisher,
            search_field="name",
            api_endpoint=reverse("async_select_search"),
        )

        # Set up crispy forms helper
        self.helper = FormHelper()
        self.helper.form_class = "form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Book Details",
                FloatingField("title", css_class="mb-2"),
                FloatingField("binding", css_class="mb-2"),
                FloatingField("publisher", css_class="mb-2"),
                Field("authors", css_class="mb-2"),
            ),
            ButtonHolder(
                Submit("submit", "Save", css_class="btn btn-primary"),
                css_class="d-flex flex-row justify-content-end w-100 mt-3",
            ),
        )
