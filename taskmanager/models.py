from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Team(models.Model):
    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
    title = models.CharField(_("title"), max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team_users', verbose_name=_('team_users'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return "[%s] %s" % (self.id, self.title)


class Task(models.Model):
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    STATUSES = (
        ('to-do', _('To Do')),
        ('in_progress', _('In Progress')),
        ('blocked', _('Blocked')),
        ('done', _('Done')),
        ('dismissed', _('Dismissed'))
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), max_length=2000, null=True, blank=True)
    resolution = models.TextField(_("resolution"), max_length=2000, null=True, blank=True)
    deadline = models.DateField(_("deadline"), null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_assigned', verbose_name=_('assigned to'),
                                   on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(_("state"), max_length=20, choices=STATUSES, default='to-do')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks_created', verbose_name=_('created by'),
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(_("last modified"), auto_now=True, editable=False)

    def __str__(self):
        return "[%s] %s" % (self.id, self.title)