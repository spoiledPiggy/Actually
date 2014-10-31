from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
# Users include developers and product managers
# give github name , return projects
# give project , return all users, and pm( at top of list)
# give a github name, return all milestones 

class Project(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000, null = True, blank = True)
	startTime = models.DateTimeField('date the project starts')
	finishTime = models.DateTimeField('date the project finishes', null = True, blank = True)
	progress = models.FloatField(default = 0)
	prevProgress =models.FloatField(default = 0)
	repo = models.CharField(max_length = 100)
	repoOwner = models.CharField(max_length = 100)

	def addProject(self, name, description, startTime, repo, repoOwner):
		self.name = name
		self.description = description
		self.startTime = startTime
		self.progress = 0
		self.repo = repo
		self.repoOwner = repoOwner
		self.save()


	def __unicode__(self):
		return self.name

	def update(self, progress):
		self.prevProgress = self.progress
		self.progress = progress
		self.save()

	def findPmDeveloperByProject(self,GivenProject):
		findProject = Project.objects.filter(name = GivenProject)
		if (len(findPM) != 0):
			PmName= PM.objects.filter(project =findProject)
			DeveloperName = Developer.objects.filter(project = findProject)
			return PmName + DeveloperName
		else:
			print 'no PM or Developer found by project'


class PM(models.Model):
	firstName = models.CharField(max_length = 50)
	lastName = models.CharField(max_length = 50)
	githubName = models.CharField(max_length =50)
	project = models.ManyToManyField(Project, null = True, blank = True)

	def __unicode__(self):
		return '{} {}'.format(self.firstName, self.lastName)

	def findProjectByPM(self, GivenGithub_name):
		#many to many
		findProjectByPM = Project.objects.filter(githubName = GivenGithub_name)
		if (len(findProjectByPM) != 0):
			return findProjectByPM 
		else:
			print 'no project found by PM'

	def addPM(self, firstName, lastName, githubName, project):
		self.firstName = firstName
		self.lastName = lastName
		self.githubName = githubName
		self.project = project
		self.save()

	def findMilestoneByPM(self, GivenGithub_name):
		#many to many
		findMilestoneByPM = Milestone.objects.filter(githubName = GivenGithub_name)
		if (len(findMilestoneByPM) != 0):
			return findMilestoneByPM
		else:
			print 'no milestone found by PM'	

class Developer(models.Model):
	firstName = models.CharField(max_length = 50)
	lastName = models.CharField(max_length = 50)
	githubName = models.CharField(max_length =50, null = True, blank =True)
	pmAssigned = models.ForeignKey(PM, null = True, blank = True)
	project = models.ManyToManyField(Project, null = True, blank = True)


	def addDeveloper(self, firstName, lastName, githubName, pmAssigned, project):
		self.firstName = firstName
		self.lastName = lastName
		self.githubName = githubName
		self.pmAssigned = pmAssigned
		self.project = project
		self.save()



	def findProjectByDeveloper(self, GivenGithub_name):
		#many to many
		findDeveloperByDeveloper = Project.objects.filter(githubName=GivenGithub_name)
		if (len(findDeveloperByDeveloper) != 0):
			return findDeveloperByDeveloper
		else:
			print 'no project found by Developer'

	def findMilestonByDeveloper(self, GivenGithub_name):
		#many to many
		findMilestonByDeveloper = Project.objects.filter(githubName=GivenGithub_name)
		if (len(findMilestonByDeveloper) != 0):
			return findMilestonByDeveloper
		else:
			print 'no project found by Developer'

	def __unicode__(self):
		return '{} {}'.format(self.firstName, self.lastName)


class Milestone(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000, null = True, blank = True)
	progress = models.FloatField(default = 0)
	prevProgress = models.FloatField(default = 0)
	percentage = models.FloatField()
	dueDate = models.DateTimeField()

	def addMilestone(self, name, description, dueDate, percentage):
		self.name = name
		self.description = description
		self.dueDate = datetime.now()
		self.percentage = percentage
		self.save()


	def __unicode__(self):
		return self.name

	def update(self, progress):
		self.prevProgress = self.progress
		section = Section.objects.all()
		prog = 0
		for sec in section:
			prog = prog + sec.percentage
		self.progress = self.progress + progress/prog
		self.save()

class Section(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000, null = True, blank = True)
	percentage = models.FloatField('the percentage in the the project')
	progress = models.FloatField(default = 0)
	prevProgress = models.FloatField(default = 0)
	developer = models.ForeignKey(Developer, null = True, blank = True)
	project = models.ForeignKey(Project)
	milestone = models.ForeignKey(Milestone)

	def __unicode__(self):
		return self.name

	def update(self, progress):
		self.prevProgress = self.progress
		self.progress = self.progress + progress
		progressUpdate = self.percentage * progress 
		self.project.update(progressUpdate)
		self.milestone.update(progressUpdate)
		self.save()

	# def search_finished_section():
	# 	pass


class Task(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 1000, null = True, blank = True)
	percentage = models.FloatField('the percentage in the the section')
	progress = models.FloatField(default = 0)
	prevProgress = models.FloatField(default = 0)
	section = models.ForeignKey(Section)

	def update(self, progress):
		self.prevProgress = self.progress
		self.progress = progress
		updateProgress = self.percentage * (self.progress - self.prevProgress)
		self.section.update(updateProgress)
		self.save()

	def addTask(self, name, description, percentage, section):
		self.name = name
		self.description = description
		self.percentage = percentage
		self.section = section
		self.save()


	def __unicode__(self):
		return self.name

class Commit(models.Model):
	commitTime = models.DateTimeField()
	progress = models.FloatField()
	developer = models.ForeignKey(Developer)
	project = models.ForeignKey(Project)
	task = models.ForeignKey(Task)

	def __unicode__(self):
		return '{} {} {} {:.2f} {}'.format(self.developer.firstName, self.developer.lastName, 
			self.task.name, self.progress, self.commitTime)

	# def addCommit(self, commitTime, progress, developer, project, task):
	# 	self.commitTime = commitTime
	# 	self.progress = progress
	# 	self.developer = developer
	# 	self.project = project
	# 	self.task = task
	# 	self.save()






















