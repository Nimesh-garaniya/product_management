from datetime import datetime, timedelta
from urllib import request

from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.views import LoginRequiredMixin
from .models import Category, Product
from .forms import CategoryForm, ProductForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.list import ListView


class CategoryList(ListView, LoginRequiredMixin):
    model = Category
    context_object_name = "data"
    template_name = "list_view.html"


class CategoryCreate(CreateView, LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    template_name = "create_view.html"
    success_url = reverse_lazy('product:CategoryList')

    def form_valid(self, form):
        self.object = form.save()

        messages.success(self.request, 'category added successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category details invalid')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(CategoryCreate, self).get_context_data(**kwargs)
        # add data
        ctx['title'] = "Category Create Page"
        ctx['header'] = "Category Create"
        return ctx


class CategoryUpdate(UpdateView, LoginRequiredMixin):
    model = Category
    form_class = CategoryForm
    template_name = "update_view.html"
    success_url = reverse_lazy('product:CategoryList')

    def form_valid(self, form):
        self.object = form.save()

        messages.success(self.request, 'category updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Category details invalid')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(CategoryUpdate, self).get_context_data(**kwargs)
        ctx['title'] = "Category Update Page"
        ctx['header'] = "Category Update"
        return ctx


class CategoryDelete(DeleteView, LoginRequiredMixin):
    model = Category
    success_url = reverse_lazy('product:CategoryList')
    template_name = "delete_view.html"

    def get_context_data(self, **kwargs):
        ctx = super(CategoryDelete, self).get_context_data(**kwargs)
        # add data
        ctx['title'] = "Category Delete Page"
        ctx['header'] = "Category Delete"
        return ctx


class ProductList(ListView, LoginRequiredMixin):
    model = Product
    context_object_name = "data"
    template_name = "product_list_view.html"

    def email_value(value):
        email = value.split().split()[1]
        var = name.split('@')[0]
        context['var'] = var


class ProductCreate(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = "create_view.html"
    success_url = reverse_lazy('product:ProductList')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user
        self.object.save()
        messages.success(self.request, 'product added successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'product details invalid')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['title'] = "Product Create Page"
        ctx['header'] = "Product Create"
        return ctx


class ProductUpdate(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = "update_view.html"
    success_url = reverse_lazy('product:ProductList')

    def form_valid(self, form):
        obj = form.save(commit=False)
        price = Product.objects.get(id=obj.pk).price
        # abc = Product.objects.filter().values("price").first()

        if 'price' in form.changed_data:
            increase_price = price + (price * 0.1)
            decrease_price = price - (price * 0.1)
            if obj.price > increase_price:
                messages.warning(self.request, "Cannot Increase price more than 10%")
            elif obj.price < decrease_price:
                messages.warning(self.request, "Cannot Decrease price less than 10%")
                return super(ProductUpdate, self).form_invalid(form)

            if obj.price_updated:
                if not (datetime.utcnow() - obj.price_updated.replace(tzinfo=None)) > timedelta(1):
                    messages.error(self.request, "Price can only be updated once in a Day!!")
                    return redirect("product:ProductList")
                else:
                    obj.price_updated = datetime.now()
                    obj.save()
                    return super(ProductUpdate, self).form_valid(form)
            else:
                obj.price_updated = datetime.now()
                obj.save()
        form.save()
        messages.success(self.request, 'Product Updated Successfully')
        return super(ProductUpdate, self).form_valid(form)

    # def post(self):
    #     abc = Product.objects.filter().values("price").first()
    #     print(abc)

    def form_invalid(self, form):
        messages.error(self.request, 'Product details invalid')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['title'] = "Product Update Page"
        ctx['header'] = "Product Update"
        return ctx


class ProductDelete(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('product:ProductList')
    template_name = "delete_view.html"

    def get_context_data(self, **kwargs):
        ctx = super(ProductDelete, self).get_context_data(**kwargs)
        # add data
        ctx['title'] = "Product Delete Page"
        ctx['header'] = "Product Delete"
        return ctx

