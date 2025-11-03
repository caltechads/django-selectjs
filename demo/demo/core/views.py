from book_manager.models import Book
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from wildewidgets import (
    Block,
    BreadcrumbBlock,
    CardWidget,
    CrispyFormWidget,
    PageHeader,
)

from demo.core.forms import BookForm

from .wildewidgets import BaseBreadcrumbs, BookModelTable, DemoStandardMixin


class WildewidgetsView(DemoStandardMixin, TemplateView):
    menu_item: str = "Home"

    def get_content(self) -> Block:
        return Block(
            PageHeader(
                header_text="Books",
                badge_text=Book.objects.count(),
                badge_class="success",
            ),
            CardWidget(widget=BookModelTable()),
        )

    def get_breadcrumbs(self) -> BreadcrumbBlock:
        breadcrumbs = BaseBreadcrumbs()
        breadcrumbs.add_breadcrumb("Django SelectJS Demo")
        return breadcrumbs


class BookEditView(DemoStandardMixin, UpdateView):
    menu_item: str = "Home"
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("core:home")

    def get_content(self) -> Block:
        return Block(
            PageHeader(
                header_text="Edit Book",
            ),
            CardWidget(widget=CrispyFormWidget()),
        )

    def get_breadcrumbs(self) -> BreadcrumbBlock:
        breadcrumbs = BaseBreadcrumbs()
        breadcrumbs.add_breadcrumb("Django SelectJS Demo")
        return breadcrumbs
