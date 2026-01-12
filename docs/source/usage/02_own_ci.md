# Use in your own CI job

## In Zuul
The Framework exposes various jobs you may re-use as parent. Please have a look
at the [zuul.d](https://github.com/openstack-k8s-operators/ci-framework/tree/main/zuul.d)
content for more details.

### Special parameters
If you consume the [existing playbooks](https://github.com/openstack-k8s-operators/ci-framework/tree/main/ci/playbooks),
you may have to pass down some extra parameters, for instance in order to point
to your own scenarios, or any of the environment specificities you need to
address.

Worry not, there's a way! Passing `cifmw_extras` parameter from your Zuul job
definition, you can pass any kind of parameters as a list:
~~~{code-block} YAML
:caption: zuul.d/job.yaml
:linenos:
- job:
    name: cifmw-end-to-end
    parent: cifmw-end-to-end-base
    files:
      - ^roles/.*_build/(?!meta|README).*
      - ^roles/build.*/(?!meta|README).*
      - ^roles/openshift_*/(?!meta|README).*
      - ^playbooks/.*build.*.yml
    irrelevant-files:
      - ^.*/*.md
      - ^ci/templates
    vars:
      cifmw_extras:
        - '@scenarios/centos-9/ci-build.yml'
    run: ci/playbooks/e2e-run.yml
~~~

Here, the custom environment file "edpm-ansible.yml" will be passed down to the
playbook.

By the way, you may inherit from this very job since it's exposed from within
the ci-framework!
